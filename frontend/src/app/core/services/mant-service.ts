import { Injectable } from '@angular/core';
import { Mantenimiento } from '../interfaces/mantenimiento';
import { HttpClient } from '@angular/common/http';
import { map, Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class MantService {
  private baseUrl = 'http://localhost:8000/api/mantenimientos';

  constructor(private http: HttpClient) {}
  
  getAll(): Observable<Mantenimiento[]> {
    const res$ = this.http.get<Mantenimiento[]>(this.baseUrl);
    res$.subscribe(data => console.log('Datos recibidos de alq:', data));
    return res$;
  }


  create(mantenimiento: Mantenimiento) {
    const payload = {
          ...mantenimiento,
        };
    return this.http.post<Mantenimiento>(this.baseUrl, payload).pipe(
      map(a => ({
        ...a
      }))
    );
  }
  
}
