import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { Vehiculo } from '../../core/interfaces/vehiculo';

@Injectable({ providedIn: 'root' })
export class VehiculosService {
  private baseUrl = 'http://localhost:8000/api/vehiculos';

  constructor(private http: HttpClient) {}

  getAll(): Observable<Vehiculo[]> {
    const res$ = this.http.get<Vehiculo[]>(this.baseUrl);
    res$.subscribe(data => console.log('Datos recibidos:', data));
    return res$;
    /*
    var mockVehiculos :Vehiculo[] = [
      { id_vehiculo: 1, marca: 'Toyota', modelo: 'Corolla', anio: 2020, patente: 'AB123CD', tipo: 'Auto', kilometraje: 45000, disponible: true, costo_diario: 18000, estado: 'Excelente' },
      { id_vehiculo: 2, marca: 'Volkswagen', modelo: 'Gol Trend', anio: 2018, patente: 'AC456EF', tipo: 'Auto', kilometraje: 72000, disponible: true, costo_diario: 15000, estado: 'Bueno' },
      { id_vehiculo: 3, marca: 'Chevrolet', modelo: 'Onix', anio: 2021, patente: 'AD789GH', tipo: 'Auto', kilometraje: 30000, disponible: false, costo_diario: 20000, estado: 'Excelente' },
      { id_vehiculo: 4, marca: 'Ford', modelo: 'EcoSport', anio: 2019, patente: 'AE321JK', tipo: 'SUV', kilometraje: 60000, disponible: true, costo_diario: 25000, estado: 'Muy bueno' },
      { id_vehiculo: 5, marca: 'Renault', modelo: 'Kangoo', anio: 2017, patente: 'AF654LM', tipo: 'Utilitario', kilometraje: 110000, disponible: true, costo_diario: 22000, estado: 'Bueno' },
      { id_vehiculo: 6, marca: 'Peugeot', modelo: '208', anio: 2022, patente: 'AG987NP', tipo: 'Auto', kilometraje: 15000, disponible: true, costo_diario: 23000, estado: 'Excelente' },
      { id_vehiculo: 7, marca: 'Fiat', modelo: 'Cronos', anio: 2021, patente: 'AH741QR', tipo: 'Auto', kilometraje: 28000, disponible: false, costo_diario: 19000, estado: 'Muy bueno' },
      { id_vehiculo: 8, marca: 'Nissan', modelo: 'Kicks', anio: 2020, patente: 'AI852ST', tipo: 'SUV', kilometraje: 50000, disponible: true, costo_diario: 26000, estado: 'Muy bueno' },
      { id_vehiculo: 9, marca: 'Ford', modelo: 'Ranger', anio: 2019, patente: 'AJ963UV', tipo: 'Pick-Up', kilometraje: 85000, disponible: true, costo_diario: 35000, estado: 'Bueno' },
      { id_vehiculo: 10, marca: 'Mercedes-Benz', modelo: 'Sprinter', anio: 2018, patente: 'AK159WX', tipo: 'Utilitario', kilometraje: 140000, disponible: false, costo_diario: 40000, estado: 'Bueno' },
      { id_vehiculo: 11, marca: 'Honda', modelo: 'Civic', anio: 2020, patente: 'AL753YZ', tipo: 'Auto', kilometraje: 38000, disponible: true, costo_diario: 24000, estado: 'Excelente' },
      { id_vehiculo: 12, marca: 'Jeep', modelo: 'Renegade', anio: 2021, patente: 'AM246BC', tipo: 'SUV', kilometraje: 32000, disponible: true, costo_diario: 27000, estado: 'Excelente' }
    ];
    return of(mockVehiculos);*/

  }

  getById(id: number): Observable<Vehiculo> {
    return this.http.get<Vehiculo>(`${this.baseUrl}/${id}`);
  }

  create(vehiculo: Vehiculo): Observable<Vehiculo> {
    return this.http.post<Vehiculo>(this.baseUrl, vehiculo);
  }

  update(vehiculo: Vehiculo): Observable<Vehiculo> {
    return this.http.put<Vehiculo>(`${this.baseUrl}/${vehiculo.id_vehiculo}`, vehiculo);
  }

  delete(id: number): Observable<void> {
    return this.http.delete<void>(`${this.baseUrl}/${id}`);
  }
}