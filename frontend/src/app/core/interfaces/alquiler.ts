import { Cliente } from "./cliente";
import { Empleado } from "./empleado";
import { Vehiculo } from "./vehiculo";

export interface Alquiler {
    id_alquiler: number;
    id_cliente: number;
    cliente: Cliente; // asigno
    id_vehiculo: number;
    vehiculo: Vehiculo; // asigno
    id_empleado: number;
    empleado: Empleado; // se lo coloco con la sesion iniciada
    fecha_inicio?: Date; // no te lo asigno, lo asigna la bd
    fecha_fin?: Date;
    costo_total?: number;
    kilometraje_inicial: number;
    kilometraje_final?: number;
    estado: string;
}