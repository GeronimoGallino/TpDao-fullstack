import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class RepAlqCliService {

  private baseUrl = 'http://localhost:8000/api/alquileres/cliente';

  constructor(private http: HttpClient) {}

  // GET que consulta el backend enviando el ID del cliente
  getByCliente(idCliente: number): Observable<any[]> {
    // Para usar el backend real:
    // return this.http.get<any[]>(`${this.baseUrl}/${idCliente}`);

    // Mock de datos para probar

    console.log(`Mock: obteniendo alquileres para el cliente ID ${idCliente}`);

    const mockAlquileres: any[] = [
      {
        "fecha_inicio": "2025-11-22T22:02:18.198132",
        "fecha_fin": null,
        "costo_total": null,
        "estado": "activo",
        "kilometraje_inicial": 50000,
        "kilometraje_final": null,
        "vehiculo": {
            "marca": "Toyota",
            "modelo": "Yaris",
            "patente": "OYI010"
        },
        "empleado": {
            "nombre": "Carlos Méndez"
        }
    },
    {
        "fecha_inicio": "2025-11-22T22:03:37.515844",
        "fecha_fin": null,
        "costo_total": null,
        "estado": "activo",
        "kilometraje_inicial": 50000,
        "kilometraje_final": null,
        "vehiculo": {
            "marca": "Toyota",
            "modelo": "Corolla",
            "patente": "AB123CD"
        },
        "empleado": {
            "nombre": "Geronimo Perez"
        }
    }
  ];
    
    return of(mockAlquileres);
  }
}
