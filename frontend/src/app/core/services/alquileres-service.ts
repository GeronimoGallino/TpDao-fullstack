import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, map, of } from 'rxjs';
import { Alquiler } from '../interfaces/alquiler';

@Injectable({
  providedIn: 'root',
})
export class AlquileresService {
  private baseUrl = '/api/alquileres';

  constructor(private http: HttpClient) {}

  getAll(): Observable<Alquiler[]> {
    /*
    return this.http.get<Alquiler[]>(this.baseUrl).pipe(
      map(list =>
        (list || []).map(a => ({
          ...a,
          fecha_inicio: a?.fecha_inicio ? new Date(a.fecha_inicio as any) : new Date(),
          fecha_fin: a?.fecha_fin ? new Date(a.fecha_fin as any) : new Date()
        }))
      )
    );*/
    var mockAlquileres: Alquiler[] = [ 
      { id_alquiler: 1, id_cliente: 3, cliente: { id_cliente: 3, nombre: 'Carlos Rodríguez', dni: '34567890', telefono: '3512345680', email: 'carlos.rodriguez@example.com', direccion: 'Calle Libertad 456, Córdoba', fecha_registro: new Date('2025-11-18') }, id_vehiculo: 1, vehiculo: { id_vehiculo: 1, marca: 'Toyota', modelo: 'Corolla', anio: 2020, patente: 'AB123CD', tipo: 'Auto', kilometraje: 45000, disponible: true, costo_diario: 18000, estado: 'Excelente' }, id_empleado: 2, empleado: { id_empleado: 2, nombre: 'Luis Fernández', dni: '23456781', cargo: 'Empleado', telefono: '3512222222', email: 'luis.fernandez@example.com', fecha_inicio: new Date('2022-05-10'), id_negocio: 1, negocio: { id_negocio: 1, nombre: 'Alquiler Córdoba', direccion: 'Calle Falsa 123, Córdoba', telefono: '3511234567', email: 'contacto@alquilercba.com', cuit: '30-12345678-9', fecha_inicio: new Date('2018-05-01') } }, fecha_inicio: new Date('2025-11-10'), fecha_fin: new Date('2025-11-15'), costo_total: 90000, kilometraje_inicio: 45000, kilometraje_fin: 45700, estado: 'Finalizado' }, 
      { id_alquiler: 2, id_cliente: 8, cliente: { id_cliente: 8, nombre: 'Valentina Romero', dni: '89012345', telefono: '3512345685', email: 'valentina.romero@example.com', direccion: 'Calle Córdoba 159, Córdoba', fecha_registro: new Date('2025-11-18') }, id_vehiculo: 6, vehiculo: { id_vehiculo: 6, marca: 'Peugeot', modelo: '208', anio: 2022, patente: 'AG987NP', tipo: 'Auto', kilometraje: 15000, disponible: true, costo_diario: 23000, estado: 'Excelente' }, id_empleado: 1, empleado: { id_empleado: 1, nombre: 'Ana García', dni: '12345670', cargo: 'Administrador', telefono: '3511111111', email: 'ana.garcia@example.com', fecha_inicio: new Date('2023-01-15'), id_negocio: 1, negocio: { id_negocio: 1, nombre: 'Alquiler Córdoba', direccion: 'Calle Falsa 123, Córdoba', telefono: '3511234567', email: 'contacto@alquilercba.com', cuit: '30-12345678-9', fecha_inicio: new Date('2018-05-01') } }, fecha_inicio: new Date('2025-11-01'), kilometraje_inicio: 15000, estado: 'En curso' }, 
      { id_alquiler: 3, id_cliente: 11, cliente: { id_cliente: 11, nombre: 'Diego Torres', dni: '11223344', telefono: '3512345688', email: 'diego.torres@example.com', direccion: 'Calle Tucumán 963, Córdoba', fecha_registro: new Date('2025-11-18') }, id_vehiculo: 9, vehiculo: { id_vehiculo: 9, marca: 'Ford', modelo: 'Ranger', anio: 2019, patente: 'AJ963UV', tipo: 'Pick-Up', kilometraje: 85000, disponible: true, costo_diario: 35000, estado: 'Bueno' }, id_empleado: 7, empleado: { id_empleado: 7, nombre: 'Laura Jiménez', dni: '78901236', cargo: 'Administrador', telefono: '3517777777', email: 'laura.jimenez@example.com', fecha_inicio: new Date('2022-02-28'), id_negocio: 3, negocio: { id_negocio: 3, nombre: 'Alquiler Centro', direccion: 'Calle San Martín 789, Córdoba', telefono: '3513456789', email: 'contacto@alquilercentro.com', cuit: '30-11223344-5', fecha_inicio: new Date('2020-01-20') } }, fecha_inicio: new Date('2025-10-20'), fecha_fin: new Date('2025-10-27'), costo_total: 245000, kilometraje_inicio: 85000, kilometraje_fin: 86500, estado: 'Cancelado' }, 
      { id_alquiler: 4, id_cliente: 5, cliente: { id_cliente: 5, nombre: 'Miguel Sánchez', dni: '56789012', telefono: '3512345682', email: 'miguel.sanchez@example.com', direccion: 'Calle Belgrano 321, Córdoba', fecha_registro: new Date('2025-11-18') }, id_vehiculo: 4, vehiculo: { id_vehiculo: 4, marca: 'Ford', modelo: 'EcoSport', anio: 2019, patente: 'AE321JK', tipo: 'SUV', kilometraje: 60000, disponible: true, costo_diario: 25000, estado: 'Muy bueno' }, id_empleado: 8, empleado: { id_empleado: 8, nombre: 'Fernando Díaz', dni: '89012347', cargo: 'Empleado', telefono: '3518888888', email: 'fernando.diaz@example.com', fecha_inicio: new Date('2020-12-12'), id_negocio: 1, negocio: { id_negocio: 1, nombre: 'Alquiler Córdoba', direccion: 'Calle Falsa 123, Córdoba', telefono: '3511234567', email: 'contacto@alquilercba.com', cuit: '30-12345678-9', fecha_inicio: new Date('2018-05-01') } }, fecha_inicio: new Date('2025-11-05'), fecha_fin: new Date('2025-11-08'), costo_total: 75000, kilometraje_inicio: 60000, kilometraje_fin: 60650, estado: 'Finalizado' }, 
      { id_alquiler: 5, id_cliente: 1, cliente: { id_cliente: 1, nombre: 'Juan Pérez', dni: '12345678', telefono: '3512345678', email: 'juan.perez@example.com', direccion: 'Calle Falsa 123, Córdoba', fecha_registro: new Date('2025-11-18') }, id_vehiculo: 11, vehiculo: { id_vehiculo: 11, marca: 'Honda', modelo: 'Civic', anio: 2020, patente: 'AL753YZ', tipo: 'Auto', kilometraje: 38000, disponible: true, costo_diario: 24000, estado: 'Excelente' }, id_empleado: 11, empleado: { id_empleado: 11, nombre: 'Martina Alvarez', dni: '11223345', cargo: 'Empleado', telefono: '3511112121', email: 'martina.alvarez@example.com', fecha_inicio: new Date('2022-09-15'), id_negocio: 1, negocio: { id_negocio: 1, nombre: 'Alquiler Córdoba', direccion: 'Calle Falsa 123, Córdoba', telefono: '3511234567', email: 'contacto@alquilercba.com', cuit: '30-12345678-9', fecha_inicio: new Date('2018-05-01') } }, fecha_inicio: new Date('2025-11-12'), kilometraje_inicio: 38000, estado: 'En curso' } 
    ];
    return of(mockAlquileres);
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
      fecha_inicio: alquiler.fecha_inicio instanceof Date 
        ? alquiler.fecha_inicio.toISOString() 
        : alquiler.fecha_inicio,
      fecha_fin: alquiler.fecha_fin instanceof Date 
        ? alquiler.fecha_fin.toISOString() 
        : alquiler.fecha_fin
    };
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
    return this.http.put<Alquiler>(`${this.baseUrl}/${alquiler.id_alquiler}`, payload).pipe(
      map(a => ({
        ...a,
        fecha_inicio: a?.fecha_inicio ? new Date(a.fecha_inicio as any) : new Date(),
        fecha_fin: a?.fecha_fin ? new Date(a.fecha_fin as any) : new Date()
      }))
    );
  }

  finalizar(alquiler: Alquiler): Observable<Alquiler> {
    const payload = {
      ...alquiler,
      fecha_inicio: alquiler.fecha_inicio instanceof Date
        ? alquiler.fecha_inicio.toISOString()
        : alquiler.fecha_inicio,
      fecha_fin: alquiler.fecha_fin instanceof Date 
        ? alquiler.fecha_fin.toISOString()
        : alquiler.fecha_fin
    };
    return this.http.put<Alquiler>(`${this.baseUrl}/finalizar/${alquiler.id_alquiler}`, payload).pipe(
      map(a => ({
        ...a,
        kilometraje_fin: a.kilometraje_fin
      }))
    );
  }

  delete(id: number): Observable<void> {
    return this.http.delete<void>(`${this.baseUrl}/${id}`);
  }
}