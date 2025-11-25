import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class RepFacMen {
  private baseUrl = ' http://localhost:8000/api/reportes/facturacion-mensual';

  constructor(private http: HttpClient) {}

  getFacMensual(cantidad: number): Observable<any[]> {
    const res$ = this.http.get<any[]>(this.baseUrl);
    res$.subscribe(data => console.log('Datos recibidos:', data));
    return res$;
  }
}
