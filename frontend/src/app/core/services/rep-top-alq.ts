import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class RepTopAlqService {

  private baseUrl = 'http://localhost:8000/api/reportes/vehiculos-mas-alquilados?limite=';

  constructor(private http: HttpClient) {}

  // GET que consulta el backend enviando el ID del cliente
  getTopAlquileres(cantidad: number): Observable<any[]> {
    // Para usar el backend real:
    // return this.http.get<any[]>(`${this.baseUrl}/${cantidad}`);

    // Mock de datos para probar

    const mockAlquileres: any[] = [
      {
        "id": 2,
        "marca": "Toyota",
        "modelo": "Corolla",
        "patente": "AA123BB",
        "veces_alquilado": 7
      },
      {
        "id": 5,
        "marca": "Ford",
        "modelo": "Fiesta",
        "patente": "AB987CD",
        "veces_alquilado": 5
      },
      {
        "id": 1,
        "marca": "Renault",
        "modelo": "Kangoo",
        "patente": "AC456GH",
        "veces_alquilado": 3
      }
    ]

    
    return of(mockAlquileres);
  }
}
