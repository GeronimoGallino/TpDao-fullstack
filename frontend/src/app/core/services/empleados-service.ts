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
    /*
    var mockEmpleados: Empleado[] = [{ id_empleado: 1, nombre: 'Ana García', dni: '12345670', cargo: 'Administrador', telefono: '3511111111', email: 'ana.garcia@example.com', fecha_inicio: new Date('2023-01-15'), id_negocio: 1, negocio: { id_negocio: 1, nombre: 'Alquiler Córdoba', direccion: 'Calle Falsa 123, Córdoba', telefono: '3511234567', email: 'contacto@alquilercba.com', cuit: '30-12345678-9', fecha_inicio: new Date('2018-05-01') } },
        { id_empleado: 2, nombre: 'Luis Fernández', dni: '23456781', cargo: 'Empleado', telefono: '3512222222', email: 'luis.fernandez@example.com', fecha_inicio: new Date('2022-05-10'), id_negocio: 1, negocio: { id_negocio: 1, nombre: 'Alquiler Córdoba', direccion: 'Calle Falsa 123, Córdoba', telefono: '3511234567', email: 'contacto@alquilercba.com', cuit: '30-12345678-9', fecha_inicio: new Date('2018-05-01') } },
        { id_empleado: 3, nombre: 'Carla Torres', dni: '34567892', cargo: 'Empleado', telefono: '3513333333', email: 'carla.torres@example.com', fecha_inicio: new Date('2021-11-01'), id_negocio: 1, negocio: { id_negocio: 1, nombre: 'Alquiler Córdoba', direccion: 'Calle Falsa 123, Córdoba', telefono: '3511234567', email: 'contacto@alquilercba.com', cuit: '30-12345678-9', fecha_inicio: new Date('2018-05-01') } },
        { id_empleado: 4, nombre: 'Javier Ruiz', dni: '45678903', cargo: 'Administrador', telefono: '3514444444', email: 'javier.ruiz@example.com', fecha_inicio: new Date('2020-07-20'), id_negocio: 2, negocio: { id_negocio: 2, nombre: 'Alquiler Villa', direccion: 'Av. Libertad 456, Villa Allende', telefono: '3512345678', email: 'contacto@alquilervilla.com', cuit: '30-98765432-1', fecha_inicio: new Date('2019-03-15') } },
        { id_empleado: 5, nombre: 'Sofía López', dni: '56789014', cargo: 'Empleado', telefono: '3515555555', email: 'sofia.lopez@example.com', fecha_inicio: new Date('2023-03-05'), id_negocio: 2, negocio: { id_negocio: 2, nombre: 'Alquiler Villa', direccion: 'Av. Libertad 456, Villa Allende', telefono: '3512345678', email: 'contacto@alquilervilla.com', cuit: '30-98765432-1', fecha_inicio: new Date('2019-03-15') } },
        { id_empleado: 6, nombre: 'Miguel Sánchez', dni: '67890125', cargo: 'Empleado', telefono: '3516666666', email: 'miguel.sanchez@example.com', fecha_inicio: new Date('2021-08-17'), id_negocio: 3, negocio: { id_negocio: 3, nombre: 'Alquiler Centro', direccion: 'Calle San Martín 789, Córdoba', telefono: '3513456789', email: 'contacto@alquilercentro.com', cuit: '30-11223344-5', fecha_inicio: new Date('2020-01-20') } },
        { id_empleado: 7, nombre: 'Laura Jiménez', dni: '78901236', cargo: 'Administrador', telefono: '3517777777', email: 'laura.jimenez@example.com', fecha_inicio: new Date('2022-02-28'), id_negocio: 3, negocio: { id_negocio: 3, nombre: 'Alquiler Centro', direccion: 'Calle San Martín 789, Córdoba', telefono: '3513456789', email: 'contacto@alquilercentro.com', cuit: '30-11223344-5', fecha_inicio: new Date('2020-01-20') } },
        { id_empleado: 8, nombre: 'Fernando Díaz', dni: '89012347', cargo: 'Empleado', telefono: '3518888888', email: 'fernando.diaz@example.com', fecha_inicio: new Date('2020-12-12'), id_negocio: 1, negocio: { id_negocio: 1, nombre: 'Alquiler Córdoba', direccion: 'Calle Falsa 123, Córdoba', telefono: '3511234567', email: 'contacto@alquilercba.com', cuit: '30-12345678-9', fecha_inicio: new Date('2018-05-01') } },
        { id_empleado: 9, nombre: 'Valentina Romero', dni: '90123458', cargo: 'Empleado', telefono: '3519999999', email: 'valentina.romero@example.com', fecha_inicio: new Date('2023-06-01'), id_negocio: 2, negocio: { id_negocio: 2, nombre: 'Alquiler Villa', direccion: 'Av. Libertad 456, Villa Allende', telefono: '3512345678', email: 'contacto@alquilervilla.com', cuit: '30-98765432-1', fecha_inicio: new Date('2019-03-15') } },
        { id_empleado: 10, nombre: 'Gonzalo Herrera', dni: '01234569', cargo: 'Administrador', telefono: '3511010101', email: 'gonzalo.herrera@example.com', fecha_inicio: new Date('2021-04-22'), id_negocio: 3, negocio: { id_negocio: 3, nombre: 'Alquiler Centro', direccion: 'Calle San Martín 789, Córdoba', telefono: '3513456789', email: 'contacto@alquilercentro.com', cuit: '30-11223344-5', fecha_inicio: new Date('2020-01-20') } },
        { id_empleado: 11, nombre: 'Martina Alvarez', dni: '11223345', cargo: 'Empleado', telefono: '3511112121', email: 'martina.alvarez@example.com', fecha_inicio: new Date('2022-09-15'), id_negocio: 1, negocio: { id_negocio: 1, nombre: 'Alquiler Córdoba', direccion: 'Calle Falsa 123, Córdoba', telefono: '3511234567', email: 'contacto@alquilercba.com', cuit: '30-12345678-9', fecha_inicio: new Date('2018-05-01') } },
        { id_empleado: 12, nombre: 'Diego Torres', dni: '22334456', cargo: 'Empleado', telefono: '3511212121', email: 'diego.torres@example.com', fecha_inicio: new Date('2023-01-30'), id_negocio: 2, negocio: { id_negocio: 2, nombre: 'Alquiler Villa', direccion: 'Av. Libertad 456, Villa Allende', telefono: '3512345678', email: 'contacto@alquilervilla.com', cuit: '30-98765432-1', fecha_inicio: new Date('2019-03-15') } }
      ];
    return of(mockEmpleados);*/
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
    return this.http.put<Empleado>(`${this.baseUrl}/${emp.id_empleado}`, payload).pipe(
      map(e => ({ ...e, fecha_inicio: e?.fecha_inicio ? new Date(e.fecha_inicio as any) : new Date() }))
    );
  }

  delete(id: number): Observable<void> {
    return this.http.delete<void>(`${this.baseUrl}/${id}`);
  }
}
