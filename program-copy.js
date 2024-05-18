const readlineSync = require('readline-sync');


class Vuelo {
    #origen = '';
    #destino = '';
    #costo = 0;
    #mascota = 1;

    set origen(nuevoOrigen){
        this.#origen = nuevoOrigen;
    }
    get origen(){
        return this.#origen;
    }

    set destino(nuevoDestino){
        this.#destino = nuevoDestino;
    }
    get destino(){ 
        return this.#destino;
    }

    set costo(nuevoCosto){
        this.#costo = nuevoCosto;
    }
    get costo(){
        return this.#costo;
    }

    set mascota(nuevaMascota){
        this.#mascota = nuevaMascota;
    }
    get mascota(){
        return this.#mascota;
    }

    constructor(origen, destino, costo, mascota){
        if(origen == undefined){
            throw new Error('El origen del vuelo es requerido');}
        if(destino == undefined){
            throw new Error('El destino del vuelo es requerido');}
        if(costo == undefined){
            throw new Error('El costo del vuelo es requerido');}
        if(mascota == undefined){
            throw new Error('El campo mascota es requerido');}

        this.#origen = origen;
        this.#destino = destino;
        this.#costo = costo;
        this.#mascota = mascota;

    }
}

class NodoVuelo {
    valor = null;
    siguiente = null;
}

class ListaVuelos {
    cabeza = null;

    insertar(vuelo){
        const nuevoNodo = new NodoVuelo();
        nuevoNodo.valor = vuelo;

        if(this.cabeza === null){
            this.cabeza = nuevoNodo;
        } else {
            let nodoTmp = this.cabeza;
            while(nodoTmp.siguiente !== null){
                nodoTmp = nodoTmp.siguiente;
            }
            nodoTmp.siguiente = nuevoNodo;
        }
    }

    mostrarTodosLosVuelos(){
        if(this.cabeza == null){
            console.log(`No hay vuelos para mostrar, no hay nodos en la lista`);
        }
        else {
            let nodoTmp = this.cabeza;
            let i = 1;
            while(nodoTmp != null){
                console.log(`Datos del vuelo numero ${i}`);
                console.log(`destino: ${nodoTmp.valor.destino}:`);
                console.log(`origen: ${nodoTmp.valor.origen}:`);
                console.log(`costo: ${nodoTmp.valor.costo}:`);
                nodoTmp = nodoTmp.siguiente;
                i++;
            }
        }
    }
    
    impuestoMascota(){
        let impuestoSiMascota = 0;
        let totalImpuestoMacota = 0;

        if(this.cabeza == null){
            console.log(`No hay vuelos para mostrar, no hay nodos en la lista`);
        }
        else {
            let nodoTmp = this.cabeza;
            let i = 1;
            while(nodoTmp != null){
                if(nodoTmp.valor.mascota == 1){
                    nodoTmp.valor.impuestoSiMascota = 50000;
                    console.log(`El impuesto mascota es: ${nodoTmp.valor.impuestoSiMascota}`);
                    impuestoSiMascota += nodoTmp.valor.impuestoSiMascota;
                }
                else {
                    console.log(`El vuelo no tiene mascota`);
                    totalImpuestoMacota += nodoTmp.valor.costo + nodoTmp.valor.impuestoSiMascota;
                }

                nodoTmp = nodoTmp.siguiente;
                i++;
            }totalImpuestoMacota += impuestoSiMascota;
            console.log(`${totalImpuestoMacota}`);
            console.dir(`**********************************************************`);
            
        }
    }

    

    
    nominaTotlaItems(){
        if(this.cabeza == null){
            console.log(`No hay vuelos para mostrar, no hay nodos en la lista`);
        }
        else {
            let nodoTmp = this.cabeza;
            let i = 1;
            let totalCosto = 0;
            while(nodoTmp != null){
                totalCosto += nodoTmp.valor.costo;
                nodoTmp = nodoTmp.siguiente;
                i++;
            }
            console.log(`${totalCosto}`);
        }
    }
    

    
}



const listaVuelos = new ListaVuelos();

let continuar = true;
while(continuar){
    const origen = readlineSync.question('****** Ingrese el origen del vuelo: ');
    const destino = readlineSync.question('Ingrese el destino del vuelo: ');
    const costo = +readlineSync.question('Ingrese el costo del vuelo: ');
    const mascota = +readlineSync.question('El vuelo incluye mascota? (s(1)/n(2)): ***************** ');
    

    const vuelo = new Vuelo(destino, origen, costo, mascota);
    listaVuelos.insertar(vuelo);

    const respuesta = readlineSync.question('Desea agregar otro vuelo? (s/n): ');
    if(respuesta === 'n'){
        continuar = false;
    }
}

listaVuelos.mostrarTodosLosVuelos();
listaVuelos.impuestoMascota();

