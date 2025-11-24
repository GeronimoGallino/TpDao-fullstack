import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { Vehiculo } from '../../core/interfaces/vehiculo';

@Injectable({ providedIn: 'root' })
export class VehiculosService {
  private baseUrl = 'http://localhost:8000/api/vehiculos';

  constructor(private http: HttpClient) {}

  getAll(): Observable<Vehiculo[]> {
    const res$ = this.http.get<Vehiculo[]>(this.baseUrl);
    res$.subscribe(data => console.log('Datos recibidos:', data));
    return res$;
  }
  
  getAllActive(): Observable<Vehiculo[]> {
    const res$ = this.http.get<Vehiculo[]>(`${this.baseUrl}/activos`);
    res$.subscribe(data => console.log('Datos recibidos de vehiculos activos:', data));
    return res$;
  }

  getById(id: number): Observable<Vehiculo> {
    return this.http.get<Vehiculo>(`${this.baseUrl}/${id}`);
  }

  create(vehiculo: Vehiculo): Observable<Vehiculo> {
    return this.http.post<Vehiculo>(this.baseUrl, vehiculo);
  }

  update(vehiculo: Vehiculo): Observable<Vehiculo> {
    return this.http.put<Vehiculo>(`${this.baseUrl}/${vehiculo.id}`, vehiculo);
  }

  delete(id: number): Observable<void> {
    return this.http.delete<void>(`${this.baseUrl}/${id}`);
  }
}