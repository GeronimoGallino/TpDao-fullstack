import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, map, of } from 'rxjs';
import { Empleado } from '../../core/interfaces/empleado';

@Injectable({ providedIn: 'root' })
export class EmpleadosService {
  private baseUrl = 'http://localhost:8000/api/empleados';

  constructor(private http: HttpClient) { }

  getAll(): Observable<Empleado[]> {
    const res$ = this.http.get<Empleado[]>(this.baseUrl);
    res$.subscribe(data => console.log('Datos recibidos:', data));
    return res$;
  }

  getById(id: number): Observable<Empleado> {
    return this.http.get<Empleado>(`${this.baseUrl}/${id}`).pipe(
      map(e => ({ ...e, fecha_inicio: e?.fecha_inicio ? new Date(e.fecha_inicio as any) : new Date() }))
    );
  }

  create(emp: Empleado): Observable<Empleado> {
    const payload = {
      ...emp,
      fecha_inicio: emp.fecha_inicio instanceof Date ? emp.fecha_inicio.toISOString() : emp.fecha_inicio ?? new Date().toISOString()
    };
    return this.http.post<Empleado>(this.baseUrl, payload).pipe(
      map(e => ({ ...e, fecha_inicio: e?.fecha_inicio ? new Date(e.fecha_inicio as any) : new Date() }))
    );
  }

  update(emp: Empleado): Observable<Empleado> {
    const payload = {
      ...emp,
      fecha_inicio: emp.fecha_inicio instanceof Date ? emp.fecha_inicio.toISOString() : emp.fecha_inicio
    };
    return this.http.put<Empleado>(`${this.baseUrl}/${emp.id}`, payload).pipe(
      map(e => ({ ...e, fecha_inicio: e?.fecha_inicio ? new Date(e.fecha_inicio as any) : new Date() }))
    );
  }

  delete(id: number): Observable<void> {
    return this.http.delete<void>(`${this.baseUrl}/${id}`);
  }
}
