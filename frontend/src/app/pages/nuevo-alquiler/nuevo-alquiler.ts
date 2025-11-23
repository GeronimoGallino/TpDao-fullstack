import { Component, OnInit } from '@angular/core';
import { Alquiler } from '../../core/interfaces/alquiler';
import { Cliente } from '../../core/interfaces/cliente';
import { Empleado } from '../../core/interfaces/empleado';
import { Vehiculo } from '../../core/interfaces/vehiculo';
import { AlquileresService } from '../../core/services/alquileres-service';
import { ClientesService } from '../../core/services/clientes-service';
import { EmpleadosService } from '../../core/services/empleados-service';
import { VehiculosService } from '../../core/services/vehiculos-service';
import { FormsModule } from '@angular/forms';
import { CommonModule, DatePipe } from '@angular/common';

@Component({
  selector: 'app-nuevo-alquiler',
  standalone: true,
  templateUrl: './nuevo-alquiler.html',
  styleUrls: ['./nuevo-alquiler.css'],
  imports: [CommonModule, FormsModule],   // DatePipe NO va en imports
  providers: [DatePipe]                  // si necesitas DatePipe, púeselo aquí
})
export class NuevoAlquilerComponent implements OnInit {
  datosCorrectos() {
    if (!this.selectedAlquiler) return false;
    return this.selectedAlquiler.id_cliente > 0 &&
      this.selectedAlquiler.id_vehiculo > 0 &&
      this.selectedAlquiler.id_empleado > 0 &&
      (this.selectedAlquiler.fecha_inicio instanceof Date || !!this.selectedAlquiler.fecha_inicio) &&
      (this.selectedAlquiler.fecha_fin instanceof Date || !!this.selectedAlquiler.fecha_fin) &&
      new Date(this.selectedAlquiler.fecha_fin) >= new Date(this.selectedAlquiler.fecha_inicio) &&
      this.selectedAlquiler.kilometraje_inicio >= 0
  }

  alquileres: Alquiler[] = [];
  alquileresFiltered: Alquiler[] = [];
  filter = '';

  clientes: Cliente[] = [];
  empleados: Empleado[] = [];
  vehiculos: Vehiculo[] = [];

  selectedAlquiler: Alquiler | null = null;
  toDeleteAlquiler: Alquiler | null = null;
  loading = false;

  constructor(
    private alquileresService: AlquileresService,
    private clientesService: ClientesService,
    private empleadosService: EmpleadosService,
    private vehiculosService: VehiculosService
  ) {}

  ngOnInit(): void {
    this.newAlquiler();
    this.loadClientes();
    this.loadEmpleados();
    this.loadVehiculos();
  }

  loadClientes(): void {
    this.clientesService.getAll().subscribe({ next: list => this.clientes = list || [], error: err => console.error(err) });
  }

  loadEmpleados(): void {
    this.empleadosService.getAll().subscribe({ next: list => this.empleados = list || [], error: err => console.error(err) });
  }

  loadVehiculos(): void {
    this.vehiculosService.getAll().subscribe({ next: list => this.vehiculos = list || [], error: err => console.error(err) });
  }

  newAlquiler(): void {
    this.selectedAlquiler = {
      id_alquiler: 0,
      id_cliente: 0,
      cliente: null as any,
      id_vehiculo: 0,
      vehiculo: null as any,
      id_empleado: 0,
      empleado: null as any,
      fecha_inicio: new Date(),
      fecha_fin: new Date(),
      costo_total: 0,
      kilometraje_inicio: 0,
      kilometraje_fin: 0,
      estado: 'activo'
    };
    setTimeout(() => window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' }), 100);
  }

  saveAlquiler(): void {
    if (!this.selectedAlquiler) return;

    console.log('Guardando alquiler:', this.selectedAlquiler);

    const payload = {
      ...this.selectedAlquiler,
      fecha_inicio: this.selectedAlquiler.fecha_inicio instanceof Date
        ? this.selectedAlquiler.fecha_inicio.toISOString()
        : this.selectedAlquiler.fecha_inicio,
      fecha_fin: this.selectedAlquiler.fecha_fin instanceof Date
        ? this.selectedAlquiler.fecha_fin.toISOString()
        : this.selectedAlquiler.fecha_fin
    };

    this.alquileresService.create(payload as any).subscribe({
      next: () => { /* acción post-creación */ this.newAlquiler(); },
      error: err => console.error('Error creando alquiler', err)
    });
  }

  cancel(): void {
    this.selectedAlquiler = null;
    this.toDeleteAlquiler = null;
  }
}