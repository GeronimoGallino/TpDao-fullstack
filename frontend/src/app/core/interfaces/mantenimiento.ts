import { Vehiculo } from "./vehiculo";
import { Empleado } from "./empleado";

export interface Mantenimiento {
  id_mantenimiento: number;
  id_vehiculo: number;
  vehiculo: Vehiculo
  id_empleado: number;
  empleado: Empleado;
  fecha: Date;
  tipo: string;
  costo: number;
  observaciones: string;
}