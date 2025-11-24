import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class RepTopAlqService {

  private baseUrl = 'http://localhost:8000/api/reportes/vehiculos-mas-alquilados';

  constructor(private http: HttpClient) {}

  getTopAlquileres(cantidad: number): Observable<any[]> {
    const res$ = this.http.get<any[]>(`${this.baseUrl}?limite=${cantidad}`);
    res$.subscribe(data => console.log('Datos recibidos:', data));
    return res$;
  }
}
