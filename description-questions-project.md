 Enunciado del Proyecto                                                                                                                                                                                                                
                                                                                                                                                                                                                                        
  Este es un Sistema de Reservas de Vuelos construido con arquitectura de microservicios usando Python/FastAPI. Implementa el patrón Vertical Slice Architecture + CQRS donde cada funcionalidad (vuelos, reservas, agente IA) es un    
  módulo independiente con sus propios modelos, esquemas, comandos y consultas.                                                                                                                                                         
                                                                                                                                                                                                                                        
  La aplicación permite gestionar destinos, vuelos y reservas con lógica de negocio que incluye cálculo automático de precios con descuentos promocionales (10%), impuestos por destino y validación de mascotas. Cuando se crea una    
  reserva, el precio se calcula en tiempo real y se despacha un evento asíncrono a RabbitMQ, que es procesado por un worker de Celery para actualizar estadísticas en Redis (ingresos totales, popularidad de destinos, distribución de 
  dulces a menores de 12 años).
                                                                                                                                                                                                                                        
  Integra un agente de Inteligencia Artificial usando el patrón RAG (Retrieval-Augmented Generation) con LangChain + Groq (Llama 3.3 70B) que consulta datos reales de PostgreSQL y Redis para responder preguntas sobre vuelos y       
  sugerir ajustes de precios basados en demanda.                                                                                                                                                                                        
                                                                                                                                                                                                                                        
  La infraestructura incluye contenedorización con Docker (multi-stage build, usuario no-root), orquestación con Kubernetes + Helm (autoescalado horizontal HPA de 2 a 10 réplicas al 70% CPU), y un pipeline CI/CD con GitHub Actions  
  de 3 etapas: tests, build/push a ghcr.io, y deploy automático al cluster.

  ---
  20 Preguntas de Entrevista con Respuestas

  1. ¿Qué patrón arquitectónico usa el proyecto y por qué?

  Vertical Slice Architecture + CQRS. Cada feature (flights, bookings, ai) es un módulo autocontenido con modelos, schemas, commands y queries. CQRS separa las operaciones de lectura (queries) de las de escritura (commands). Se
  eligió porque reduce el acoplamiento entre features, facilita la escalabilidad y permite que cada módulo evolucione independientemente.

  2. ¿Cómo se calcula el precio de una reserva?

  Se toma el base_price del vuelo. Si el destino tiene promoción activa (is_promotion=True), se aplica un 10% de descuento (base_price * 0.90). Luego se suma el impuesto del destino (tax_amount). Fórmula: total_price = (base_price *
   0.90 si hay promo) + tax_amount. Ejemplo: base 1000, promo 10% = 900, tax 50 = 950.

  3. ¿Para qué se usa Celery y RabbitMQ en este sistema?

  Para procesamiento asíncrono. Cuando se crea una reserva, la API responde inmediatamente al usuario y despacha un evento a RabbitMQ. El worker de Celery consume ese evento y actualiza estadísticas en Redis (ingresos, popularidad,
  distribución de dulces a infantes). Esto desacopla la respuesta al usuario del procesamiento secundario.

  4. ¿Qué pasa si un pasajero menor de 12 años hace una reserva?

  El worker de Celery detecta que passenger_age < 12 y automáticamente registra una distribución de dulce con costo de 5.0. Actualiza stats:total_candy_cost y stats:total_infant_count en Redis, y agrega un log a la lista
  logs:candy_distribution con el mensaje "Reserva {id}: Dulce entregado a {nombre}".

  5. ¿Cómo funciona la validación de mascotas?

  En bookings/commands.py, al crear una reserva, si has_pet=True se verifica destination.allows_pets. Si el destino no permite mascotas, se lanza un ValueError que el router convierte en HTTP 400 con el mensaje "El destino {nombre}
  no acepta mascotas".

  6. ¿Qué es el patrón RAG y cómo lo implementas?

  RAG (Retrieval-Augmented Generation) combina recuperación de datos con generación de texto por IA. En este proyecto: (1) Retrieval: dos herramientas de LangChain consultan PostgreSQL (datos de mercado) y Redis (estadísticas de
  demanda), (2) Augmentation: los datos se inyectan en el prompt, (3) Generation: Groq/Llama 3.3 genera una respuesta contextualizada con datos reales.

  7. ¿Por qué usas @functools.lru_cache(maxsize=1) para el agente de IA?

  Implementa el patrón Singleton. Crea una sola instancia de ChatGroq y la reutiliza en todas las peticiones. Evita crear conexiones redundantes al API de Groq, reduce latencia y consumo de recursos.

  8. ¿Qué ventajas tiene el Dockerfile multi-stage?

  La primera etapa (builder) instala compiladores y dependencias de build (~1.2GB). La segunda etapa copia solo los paquetes compilados sobre una imagen slim (~200MB). Resultado: imagen final más pequeña, sin herramientas de
  compilación (menor superficie de ataque), despliegue más rápido.

  9. ¿Por qué el contenedor corre con un usuario no-root?

  Es una práctica de seguridad. Si un atacante compromete la aplicación, no tendrá privilegios de root dentro del contenedor. Se crea appuser con adduser --system y se ejecuta con USER appuser.

  10. ¿Cómo funciona el HPA en Kubernetes?

  El Horizontal Pod Autoscaler monitorea el uso de CPU de los pods del deployment flight-system-api. Mantiene un mínimo de 2 réplicas (alta disponibilidad) y escala hasta 10. Cuando el promedio de CPU supera el 70%, crea nuevos pods
   automáticamente. Cuando baja, los reduce.

  11. ¿Qué hace task_acks_late=True en la configuración de Celery?

  Indica que el worker envía el ACK (acknowledgment) después de completar la tarea, no al recibirla. Si el worker muere durante el procesamiento, RabbitMQ reencola el mensaje. Esto garantiza que no se pierdan tareas.

  12. ¿Cómo se manejan las variables sensibles en Kubernetes?

  Se separan en dos recursos: ConfigMap para variables no sensibles (DATABASE_URL, REDIS_HOST) y Secret para variables sensibles (GROQ_API_KEY), que se codifica en base64 con b64enc. Los pods las consumen vía envFrom con
  configMapRef y secretRef.

  13. ¿Qué diferencia hay entre liveness y readiness probes?

  - Liveness probe: Verifica que el contenedor está vivo. Si falla 3 veces, Kubernetes mata y reinicia el pod. Configurado cada 30s.
  - Readiness probe: Verifica que el pod puede recibir tráfico. Si falla, Kubernetes deja de enviarle requests pero no lo mata. Configurado cada 10s.

  14. ¿Por qué usas pool_pre_ping=True en SQLAlchemy?

  Valida que la conexión a PostgreSQL esté activa antes de usarla. Si la conexión se cerró (por timeout, reinicio de DB, etc.), SQLAlchemy descarta esa conexión y crea una nueva. Evita errores de "connection closed" en producción.

  15. ¿Cómo funciona el pipeline CI/CD?

  Tiene 3 etapas: (1) Test: ejecuta pytest contra PostgreSQL en GitHub Actions. (2) Build & Push: solo en push a master, construye la imagen Docker y la sube a ghcr.io con el SHA del commit como tag. (3) Deploy: si existe
  KUBECONFIG, ejecuta helm upgrade --install con el tag del commit para desplegar al cluster.

  16. ¿Por qué usas worker_prefetch_multiplier=1 en Celery?

  Limita al worker a obtener una sola tarea a la vez de la cola. Evita que un worker acapare múltiples tareas mientras otros están ociosos. Mejora la distribución de carga cuando hay múltiples workers.

  17. ¿Cómo usa Redis este sistema?

  Redis cumple dos roles: (1) Almacén de estadísticas: contadores con INCRBYFLOAT para ingresos, popularidad de destinos, reservas con mascotas, costo de dulces. (2) Backend de resultados de Celery: almacena el resultado de tareas
  completadas. Las claves siguen el patrón stats:destination:{nombre} y se escanean con SCAN (paginación segura).

  18. ¿Qué validaciones hace Pydantic v2 en este proyecto?

  - passenger_age: debe estar entre 0 y 150 (usa @field_validator)
  - base_price: debe ser mayor a 0
  - tax_amount: debe ser mayor o igual a 0
  - from_attributes=True en ConfigDict permite serializar objetos SQLAlchemy directamente a JSON

  19. ¿Qué pasa si el API de Groq falla o no hay API key?

  Si GROQ_API_KEY no está configurada, get_ai_agent() lanza un RuntimeError al inicializar. Si el API falla en runtime, los endpoints /ai/chat y /ai/suggest-price capturan la excepción con try-except, registran el traceback con
  logger.exception() y retornan HTTP 500 con un mensaje genérico en español.

  20. ¿Qué mejoras le harías al sistema para producción?

  - Autenticación/Autorización: JWT o API keys (actualmente todo es público)
  - Rate limiting: middleware para proteger endpoints costosos (especialmente IA)
  - Migraciones de DB: usar Alembic en lugar de create_all()
  - Tests de Celery y Redis: verificar el flujo asíncrono completo
  - Persistencia en Redis: habilitar AOF/RDB (los datos se pierden al reiniciar)
  - CORS middleware: configurar orígenes permitidos
  - Monitoreo: alertas sobre métricas de Prometheus
  - Externalizar credenciales: mover las de RabbitMQ a secrets de Kubernetes

  ---
  Roles para Buscar Empleo

  Este proyecto es para aplicar a:
  ┌─────────────────────────────────┬────────────────────────────────────────────────────────────────────┐
  │               Rol               │                           Justificación                            │
  ├─────────────────────────────────┼────────────────────────────────────────────────────────────────────┤
  │ Backend Developer (Python)      │ FastAPI, SQLAlchemy, Pydantic, REST APIs                           │
  ├─────────────────────────────────┼────────────────────────────────────────────────────────────────────┤
  │ DevOps Engineer                 │ Docker, Kubernetes, Helm, CI/CD, GitHub Actions                    │
  ├─────────────────────────────────┼────────────────────────────────────────────────────────────────────┤
