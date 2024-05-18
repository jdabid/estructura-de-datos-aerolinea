const readlineSync = require('readline-sync');


class Vuelo {
    #origen = '';
    #destino = '';
    #impuestoDestino = 0;
    #costo = 0;
    #mascota = 1;
    #promocion = 0;
    #infante = 1;

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

    set impuestoDestino(nuevoImpuestoDestino){
        this.#impuestoDestino = nuevoImpuestoDestino;
    }
    get impuestoDestino(){
        return this.#impuestoDestino;
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

    set promocion(nuevaPromocion){
        this.#promocion = nuevaPromocion;
    }
    get promocion(){
        return this.#promocion;
    }

    set infante(nuevainfante){
        this.#infante = nuevainfante;
    }
    get infante(){
        return this.#infante;
    }

    constructor(origen, destino, impuestoDestino, costo, mascota, promocion, infante){
        if(origen == undefined){
            throw new Error('El origen del vuelo es requerido');}
        if(destino == undefined){
            throw new Error('El destino del vuelo es requerido');}
        if(impuestoDestino == undefined){
            throw new Error('El impuesto del destino es requerido');}
        if(costo == undefined){
            throw new Error('El costo del vuelo es requerido');}
        if(mascota == undefined){
            throw new Error('El campo mascota es requerido');}
        if(promocion == undefined){
            throw new Error('El campo promocion es requerido');}
        if(infante == undefined){
            throw new Error('El campo infante es requerido');}

        this.#origen = origen;
        this.#destino = destino;
        this.#impuestoDestino = impuestoDestino;
        this.#costo = costo;
        this.#mascota = mascota;
        this.#promocion = promocion;
        this.#infante = infante;

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
                console.log(`origen: ${nodoTmp.valor.origen}:`);
                console.log(`destino: ${nodoTmp.valor.destino}:`);
                console.log(`impuestoDestino: ${nodoTmp.valor.impuestoDestino}:`);
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
                    nodoTmp.valor.impuestoSiMascota = nodoTmp.valor.costo * 0.1;
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

    impuestoPromocion(){
        let impuestoSiPromocion = 0;
        let totalImpuestoPromocion = 0;

        if(this.cabeza == null){
            console.log(`No hay vuelos para mostrar, no hay nodos en la lista`);
        }
        else {
            let nodoTmp = this.cabeza;
            let i = 1;
            while(nodoTmp != null){
                if(nodoTmp.valor.promocion == 1){
                    nodoTmp.valor.impuestoSiPromocion = (nodoTmp.valor.costo* 0.1);
                    nodoTmp.valor.costo = nodoTmp.valor.costo - nodoTmp.valor.impuestoSiPromocion;
                    console.log(`El impuesto con promocion es: ${nodoTmp.valor.impuestoSiPromocion}`);
                    console.log(`El costo del vuelo con promocion es: ${nodoTmp.valor.costo}`);
                    impuestoSiPromocion += nodoTmp.valor.impuestoSiPromocion;
                }
                else {
                    console.log(`El vuelo no tiene promocion`);
                    totalImpuestoPromocion += nodoTmp.valor.costo + nodoTmp.valor.totalImpuestoPromocion;
                }

                nodoTmp = nodoTmp.siguiente;
                i++;
            }totalImpuestoPromocion += impuestoSiPromocion;
            console.log(`${totalImpuestoPromocion}`);
            console.dir(`**********************************************************`);
            
        }
    }

    impuestoInfante(){
        let impuestoSiInfante = 0;
        let totalImpuestoInfante = 0;
        let cantidadInfantes = 0;
        let dulceCortesia = 50;

        if(this.cabeza == null){
            console.log(`No hay vuelos para mostrar, no hay nodos en la lista`);
        }
        else {
            let nodoTmp = this.cabeza;
            let i = 1;
            while(nodoTmp != null){
                if(nodoTmp.valor.infante == 1){
                    cantidadInfantes = +readlineSync.question('Ingrese la cantidad de niños menor a 12 años: ');
                    nodoTmp.valor.impuestoSiInfante = (cantidadInfantes * dulceCortesia);
                    console.log(`El impuesto por dulce cortsia es: ${nodoTmp.valor.impuestoSiInfante}`);
                    impuestoSiInfante += nodoTmp.valor.impuestoSiInfante;
                }
                else {
                    console.log(`El vuelo no tiene promocion`);
                    totalImpuestoInfante += nodoTmp.valor.costo + nodoTmp.valor.totalImpuestoInfante;
                }

                nodoTmp = nodoTmp.siguiente;
                i++;
            }totalImpuestoInfante += impuestoSiInfante;
            console.log(`${totalImpuestoInfante}`);
            console.dir(`**********************************************************`);
            
        }
    }
    

    

    
    costoDelVuelo(){
        if(this.cabeza == null){
            console.log(`No hay vuelos para mostrar, no hay nodos en la lista`);
        }
        else {
            let nodoTmp = this.cabeza;
            let i = 1;
            let totalCosto = 0;
            while(nodoTmp != null){
                totalCosto += nodoTmp.valor.costo + nodoTmp.valor.impuestoDestino;
                nodoTmp = nodoTmp.siguiente;
                i++;
            }
            console.log(`Costo + impuesto destino ${totalCosto}`);
        }
    }
    

    
}



const listaVuelos = new ListaVuelos();

let continuar = true;
while(continuar){
    const origen = readlineSync.question('****** Ingrese el origen del vuelo: ');
    const destino = readlineSync.question('Ingrese el destino del vuelo: ');
    const impuestoDestino = +readlineSync.question('Ingrese el impuesto del destino: ');
    const costo = +readlineSync.question('Ingrese el costo del vuelo: ');
    const mascota = +readlineSync.question('El vuelo incluye mascota? (s(1)/n(2)): ');
    const promocion = +readlineSync.question('El vuelo tiene promocion? (s(1)/n(2)): ');
    const infante = +readlineSync.question('El vuelo tiene niños menores de 12 años? (s(1)/n(2)): ***************** ');
    

    const vuelo = new Vuelo(destino, origen, impuestoDestino, costo, mascota, promocion, infante);
    listaVuelos.insertar(vuelo);

    const respuesta = readlineSync.question('Desea agregar otro vuelo? (s/n): ');
    if(respuesta === 'n'){
        continuar = false;
    }
}

listaVuelos.mostrarTodosLosVuelos();
listaVuelos.impuestoMascota();
listaVuelos.costoDelVuelo();
listaVuelos.impuestoPromocion();
listaVuelos.impuestoInfante();
