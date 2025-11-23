import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, map, of } from 'rxjs';
import { Cliente } from '../../core/interfaces/cliente';

@Injectable({ providedIn: 'root' })
export class ClientesService {
  private baseUrl = 'http://localhost:8000/api/clientes/';

  constructor(private http: HttpClient) {}

  getAll(): Observable<Cliente[]> {
    const res$ = this.http.get<Cliente[]>(this.baseUrl);
    res$.subscribe(data => console.log('Datos recibidos:', data));
    return res$;
  /*
  var mockEmpleados: Cliente[] = [
      { id_cliente: 1, nombre: 'Juan Pérez', dni: '12345678', telefono: '3512345678', email: 'juan.perez@example.com', direccion: 'Calle Falsa 123, Córdoba', fecha_registro: new Date() },
      { id_cliente: 2, nombre: 'María Gómez', dni: '23456789', telefono: '3512345679', email: 'maria.gomez@example.com', direccion: 'Avenida Siempre Viva 742, Córdoba', fecha_registro: new Date() },
      { id_cliente: 3, nombre: 'Carlos Rodríguez', dni: '34567890', telefono: '3512345680', email: 'carlos.rodriguez@example.com', direccion: 'Calle Libertad 456, Córdoba', fecha_registro: new Date() },
      { id_cliente: 4, nombre: 'Laura Fernández', dni: '45678901', telefono: '3512345681', email: 'laura.fernandez@example.com', direccion: 'Calle Mitre 789, Córdoba', fecha_registro: new Date() },
      { id_cliente: 5, nombre: 'Miguel Sánchez', dni: '56789012', telefono: '3512345682', email: 'miguel.sanchez@example.com', direccion: 'Calle Belgrano 321, Córdoba', fecha_registro: new Date() },
      { id_cliente: 6, nombre: 'Sofía López', dni: '67890123', telefono: '3512345683', email: 'sofia.lopez@example.com', direccion: 'Calle San Martín 654, Córdoba', fecha_registro: new Date() },
      { id_cliente: 7, nombre: 'Fernando Díaz', dni: '78901234', telefono: '3512345684', email: 'fernando.diaz@example.com', direccion: 'Calle Rivadavia 987, Córdoba', fecha_registro: new Date() },
      { id_cliente: 8, nombre: 'Valentina Romero', dni: '89012345', telefono: '3512345685', email: 'valentina.romero@example.com', direccion: 'Calle Córdoba 159, Córdoba', fecha_registro: new Date() },
      { id_cliente: 9, nombre: 'Gonzalo Herrera', dni: '90123456', telefono: '3512345686', email: 'gonzalo.herrera@example.com', direccion: 'Calle Junín 753, Córdoba', fecha_registro: new Date() },
      { id_cliente: 10, nombre: 'Martina Alvarez', dni: '01234567', telefono: '3512345687', email: 'martina.alvarez@example.com', direccion: 'Calle Catamarca 852, Córdoba', fecha_registro: new Date() },
      { id_cliente: 11, nombre: 'Diego Torres', dni: '11223344', telefono: '3512345688', email: 'diego.torres@example.com', direccion: 'Calle Tucumán 963, Córdoba', fecha_registro: new Date() },
      { id_cliente: 12, nombre: 'Camila Vargas', dni: '22334455', telefono: '3512345689', email: 'camila.vargas@example.com', direccion: 'Calle Mendoza 147, Córdoba', fecha_registro: new Date() }
    ];
  return of(mockEmpleados);*/
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

http://localhost:8000/api/clientes

[
    {
        "nombre": "Ana",
        "apellido": "Lopez",
        "dni": "8f498857",
        "telefono": "123456789",
        "email": "test@test.com",
        "direccion": "Calle falsa 123",
        "id_cliente": 1,
        "fecha_registro": "2025-11-22T14:05:18.316408",
        "estado": true
    }
]
