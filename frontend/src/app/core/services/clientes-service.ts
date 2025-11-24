import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, map, of } from 'rxjs';
import { Cliente } from '../../core/interfaces/cliente';

@Injectable({ providedIn: 'root' })
export class ClientesService {
  private baseUrl = 'http://localhost:8000/api/clientes';

  constructor(private http: HttpClient) { }

  getAll(): Observable<Cliente[]> {
    const res$ = this.http.get<Cliente[]>(this.baseUrl);
    res$.subscribe(data => console.log('Datos recibidos:', data));
    return res$;
  }

  getById(id: number): Observable<Cliente> {
    return this.http.get<Cliente>(`${this.baseUrl}/${id}`).pipe(
      map(c => ({ ...c, fecha_registro: c?.fecha_registro ? new Date(c.fecha_registro as any) : new Date() }))
    );
  }

  create(cliente: Cliente): Observable<Cliente> {
    const payload = {
      ...cliente,
      fecha_registro: cliente.fecha_registro
        ? (cliente.fecha_registro instanceof Date ? cliente.fecha_registro.toISOString() : cliente.fecha_registro)
        : new Date().toISOString()
    };
    return this.http.post<Cliente>(this.baseUrl, payload).pipe(
      map(c => ({ ...c, fecha_registro: c?.fecha_registro ? new Date(c.fecha_registro as any) : new Date() }))
    );
  }

  update(cliente: Cliente): Observable<Cliente> {
    const payload = {
      ...cliente,
      fecha_registro: cliente.fecha_registro instanceof Date ? cliente.fecha_registro.toISOString() : cliente.fecha_registro
    };
    return this.http.put<Cliente>(`${this.baseUrl}/${cliente.id_cliente}`, payload).pipe(
      map(c => ({ ...c, fecha_registro: c?.fecha_registro ? new Date(c.fecha_registro as any) : new Date() }))
    );
  }

  delete(id: number): Observable<void> {
    return this.http.delete<void>(`${this.baseUrl}/${id}`);
  }
}
