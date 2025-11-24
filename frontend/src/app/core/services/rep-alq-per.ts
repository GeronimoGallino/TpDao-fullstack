import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class RepAlqPerService {

  private apiUrl = 'http://localhost:8000/api/reportes/alquileres-por-periodo';

  constructor(private http: HttpClient) {}

  getAnual(anio: number): Observable<any> {
    const params = new HttpParams()
      .set('tipo', 'anual')
      .set('anio', anio);

    console.log(this.apiUrl, params);
    return this.http.get<any>(this.apiUrl, { params });
  }

  getMensual(anio: number, mes: number): Observable<any> {
    const params = new HttpParams()
      .set('tipo', 'mensual')
      .set('anio', anio)
      .set('valor', mes);
    console.log(this.apiUrl, params);
    return this.http.get<any>(this.apiUrl, { params });
  }

  getTrimestral(anio: number, trimestre: number): Observable<any> {
    const params = new HttpParams()
      .set('tipo', 'trimestral')
      .set('anio', anio)
      .set('valor', trimestre);
    console.log(this.apiUrl, params);
    return this.http.get<any>(this.apiUrl, { params });
  }

  getReporte(tipo: string, anio: number, valor?: number): Observable<any> {
    let params = new HttpParams()
      .set('tipo', tipo)
      .set('anio', anio);
    if (valor !== null && valor !== undefined) {
      params = params.set('valor', valor);
    }

    console.log(this.apiUrl, params);
    return this.http.get<any>(this.apiUrl, { params });
  }

}
