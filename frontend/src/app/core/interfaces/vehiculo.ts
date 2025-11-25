export interface Vehiculo {
    id: number;
    marca: string;
    modelo: string;
    anio: number;
    patente: string;
    tipo: string;  
    kilometraje: number;
    disponible: boolean;
    costo_diario: number;
    estado: string;
    necesita_mantenimiento: boolean;
}