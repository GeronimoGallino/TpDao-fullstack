import { Negocio } from './negocio';

export interface Empleado {
  id_empleado: number;
  nombre: string;
  dni: string;
  cargo: string;
  telefono: string;
  email: string;
  fecha_inicio: Date;
  id_negocio: number;
  negocio: Negocio;
}