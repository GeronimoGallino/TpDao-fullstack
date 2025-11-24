import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, map, of } from 'rxjs';
import { Alquiler } from '../interfaces/alquiler';

@Injectable({
  providedIn: 'root',
})
export class AlquileresService {
  private baseUrl = 'http://localhost:8000/api/alquileres';

  constructor(private http: HttpClient) {}

  getAll(): Observable<Alquiler[]> {
    const res$ = this.http.get<Alquiler[]>(this.baseUrl);
    res$.subscribe(data => console.log('Datos recibidos de alq:', data));
    return res$;
  }

  getById(id: number): Observable<Alquiler> {
    return this.http.get<Alquiler>(`${this.baseUrl}/${id}`).pipe(
      map(a => ({
        ...a,
        fecha_inicio: a?.fecha_inicio ? new Date(a.fecha_inicio as any) : new Date(),
        fecha_fin: a?.fecha_fin ? new Date(a.fecha_fin as any) : new Date()
      }))
    );
  }

  create(alquiler: Alquiler): Observable<Alquiler> {
    const payload = {
      ...alquiler,
      id_cliente: Number(alquiler.id_cliente),
      id_vehiculo: Number(alquiler.id_vehiculo),
      id_empleado: Number(alquiler.id_empleado)
    };
    console.log('Payload para crear alquiler:', payload);
    console.log('paso por acaaaaaaaa');
    return this.http.post<Alquiler>(this.baseUrl, payload).pipe(
      map(a => ({
        ...a,
        fecha_inicio: a?.fecha_inicio ? new Date(a.fecha_inicio as any) : new Date(),
        fecha_fin: a?.fecha_fin ? new Date(a.fecha_fin as any) : new Date()
      }))
    );
  }

  update(alquiler: Alquiler): Observable<Alquiler> {
    const payload = {
      ...alquiler,
      // km_final: alquiler.km_final,
      fecha_inicio: alquiler.fecha_inicio instanceof Date
        ? alquiler.fecha_inicio.toISOString()
        : alquiler.fecha_inicio,          
      fecha_fin: alquiler.fecha_fin instanceof Date
        ? alquiler.fecha_fin.toISOString()
        : alquiler.fecha_fin
    };
    return this.http.put<Alquiler>(`${this.baseUrl}/${alquiler.id}`, payload).pipe(
      map(a => ({
        ...a,
        fecha_inicio: a?.fecha_inicio ? new Date(a.fecha_inicio as any) : new Date(),
        fecha_fin: a?.fecha_fin ? new Date(a.fecha_fin as any) : new Date()
      }))
    );
  }

  finalizar(alquiler: Alquiler): Observable<Alquiler> {
    const payload = {
      kilometraje_final: alquiler.kilometraje_final
    };
    console.log('el id que se quiere mandar es', alquiler.id);
    console.log('el payload que se quiere mandar es', payload);
    return this.http.put<Alquiler>(`${this.baseUrl}/finalizar/${alquiler.id}`, payload).pipe(
      map(a => ({
        ...a,
        kilometraje_fin: a.kilometraje_final
      }))
    );
  }

  delete(id: number): Observable<void> {
    return this.http.delete<void>(`${this.baseUrl}/${id}`);
  }
}