import { Alquiler } from "./alquiler";

export interface Multa {
  id_multa: number;
  id_alquiler: number;
  alquiler: Alquiler;
  tipo: string;
  descripcion: string;
  costo: number;
  fecha: Date;
}