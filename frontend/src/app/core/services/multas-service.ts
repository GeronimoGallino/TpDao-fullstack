import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Multa } from '../interfaces/multa';

@Injectable({
  providedIn: 'root',
})
export class MultasService {
  private apiUrl = 'http://localhost:8000/api/multas';

  constructor(private http: HttpClient) { }

  getAll(): Observable<Multa[]> {
    return this.http.get<Multa[]>(this.apiUrl);
  }

  create(multa: Multa): Observable<Multa> {
    const payload = {
      id_alquiler: Number(multa.id_alquiler),
      tipo: multa.tipo,
      descripcion: multa.descripcion,
      costo: multa.costo
    }
    console.log('payload enviado', payload);
    return this.http.post<Multa>(this.apiUrl, payload);
  }

  update(multa: Multa): Observable<Multa> {
    return this.http.put<Multa>(`${this.apiUrl}/${multa.id_alquiler}`, multa);
  }

  delete(id_alquiler: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id_alquiler}`);
  }
}
