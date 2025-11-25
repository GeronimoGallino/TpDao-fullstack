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
import { Router } from '@angular/router';

@Component({
  selector: 'app-mant-pendiente-list',
  templateUrl: './mant-pendiente.html',
  styleUrls: ['./mant-pendiente.css'],
  standalone: true,
  imports: [CommonModule, FormsModule]
})
export class MantenimientosPendComponent implements OnInit {

  mantenimientos: Mantenimiento[] = [];
  mantenimientosFiltered: Mantenimiento[] = [];
  filter = '';
  loading = false;
  empleados: Empleado[] = [];
  vehiculos: Vehiculo[] = [];

  constructor(
    private mantService: MantService,
    private empleadosService: EmpleadosService,
    private vehiculosService: VehiculosService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.loadData();
  }

  redirigirMantenimiento(v: Vehiculo): void {
    this.router.navigate(
      ['/mantenimientos/nuevo'],
      { queryParams: { id_vehiculo: v.id, km_actual: v.kilometraje } }
    );
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

  // applyFilter(): void {
  //   const q = this.filter.toLowerCase().trim();

  //   let lista = this.mantenimientos.filter(m =>
  //     m.fecha && new Date(m.fecha) >= new Date()
  //   );

  //   if (!q) {
  //     this.mantenimientosFiltered = lista;
  //     return;
  //   }

  //   this.mantenimientosFiltered = lista.filter(m =>
  //     (m.tipo || '').toLowerCase().includes(q) ||
  //     (m.observaciones || '').toLowerCase().includes(q) ||
  //     (m.id_empleado + '').includes(q) ||
  //     (m.id_vehiculo + '').includes(q)
  //   );
  // }

  vehiculosPendientes: Vehiculo[] = [];

 applyFilter(): void {
  const q = this.filter.toLowerCase().trim();

  // 1) Filtrar vehículos que requieren mantenimiento
  let lista = this.vehiculos.filter(v => v.necesita_mantenimiento === true);
  console.log('Vehículos que necesitan mantenimiento:', lista);

  // 2) Si no hay texto de búsqueda, asignar directamente
  if (!q) {
    this.vehiculosPendientes = lista;
    return;
  }

  // 3) Aplicar filtro adicional por texto (marca, modelo, patente, tipo)
  this.vehiculosPendientes = lista.filter(v =>
    (v.marca || '').toLowerCase().includes(q) ||
    (v.modelo || '').toLowerCase().includes(q) ||
    (v.patente || '').toLowerCase().includes(q) ||
    (v.tipo || '').toLowerCase().includes(q)
  );

}

}
