import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MantService } from '../../core/services/mant-service';
import { Mantenimiento } from '../../core/interfaces/mantenimiento';
import { EmpleadosService } from '../../core/services/empleados-service';
import { VehiculosService } from '../../core/services/vehiculos-service';
import { Empleado } from '../../core/interfaces/empleado';
import { Vehiculo } from '../../core/interfaces/vehiculo';
import { forkJoin } from 'rxjs';

@Component({
  selector: 'app-mant-historial-list',
  templateUrl: './mant-historial.html',
  styleUrls: ['./mant-historial.css'],
  standalone: true,
  imports: [CommonModule, FormsModule]
})
export class MantenimientosListComponent implements OnInit {

  mantenimientos: Mantenimiento[] = [];
  mantenimientosFiltered: Mantenimiento[] = [];
  filter = '';
  loading = false;
  empleados: Empleado[] = [];
  vehiculos: Vehiculo[] = [];

  constructor(
    private mantService: MantService,
    private empleadosService: EmpleadosService,
    private vehiculosService: VehiculosService
  ) {}

  ngOnInit(): void {
    this.loadData();
  }

  loadData(): void {
    this.loading = true;

    forkJoin({
      mantenimientos: this.mantService.getAll(),
      empleados: this.empleadosService.getAll(),
      vehiculos: this.vehiculosService.getAll()
    }).subscribe({
      next: ({ mantenimientos, empleados, vehiculos }) => {
        this.mantenimientos = mantenimientos || [];
        this.empleados = empleados || [];
        this.vehiculos = vehiculos || [];

        this.applyFilter();
        this.loading = false;
      },
      error: (err) => {
        console.error('Error cargando datos:', err);
        this.loading = false;
      }
    });
  }

  getEmpleado(id_empleado: number): Empleado | null {
    return this.empleados.find(e => e.id === id_empleado) || null;
  }

  getVehiculo(id_vehiculo: number): Vehiculo | null {
    return this.vehiculos.find(v => v.id === id_vehiculo) || null;
  }

  applyFilter(): void {
    const q = this.filter.toLowerCase().trim();

    if (!q) {
      this.mantenimientosFiltered = [...this.mantenimientos];
      return;
    }

    this.mantenimientosFiltered = this.mantenimientos.filter(m =>
      (m.tipo || '').toLowerCase().includes(q) ||
      (m.observaciones || '').toLowerCase().includes(q) ||
      (m.id_empleado + '').includes(q) ||
      (m.id_vehiculo + '').includes(q)
    );
  }

}
