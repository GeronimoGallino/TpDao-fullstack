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
import { CommonModule, DatePipe, NgFor, NgIf } from '@angular/common';
import { Router } from '@angular/router';
import { AuthService } from '../../core/services/auth-service';
import { User } from '../../core/interfaces/user';

@Component({
  selector: 'app-nuevo-alquiler',
  standalone: true,
  templateUrl: './nuevo-alquiler.html',
  styleUrls: ['./nuevo-alquiler.css'],
  imports: [CommonModule, FormsModule, NgIf, NgFor],   
  providers: [DatePipe]                 
})
export class NuevoAlquilerComponent implements OnInit {
  
  datosCorrectos() {
    if (!this.selectedAlquiler) return false;
      return this.selectedAlquiler.id_cliente > 0 &&
      this.selectedAlquiler.id_vehiculo > 0 // &&
      // this.selectedAlquiler.id_empleado > 0
  }

  alquileres: Alquiler[] = [];
  alquileresFiltered: Alquiler[] = [];
  filter = '';

  user: User | null = null;

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
    private vehiculosService: VehiculosService,
    private router: Router,
    private authService: AuthService
  ) {}

  ngOnInit(): void {
    this.newAlquiler();
    this.loadClientes();
    this.loadEmpleados();
    this.loadVehiculos();
    this.user = this.authService.getCurrentUser();
  }

  loadClientes(): void {
    this.clientesService.getAll().subscribe({ next: list => this.clientes = list || [], error: err => console.error(err) });
  }

  loadEmpleados(): void {
    this.empleadosService.getAll().subscribe({ next: list => this.empleados = list || [], error: err => console.error(err) });
  }

  loadVehiculos(): void {
    this.vehiculosService.getAllActive().subscribe({ next: list => this.vehiculos = list || [], error: err => console.error(err) });
  }


  newAlquiler(): void {
    this.selectedAlquiler = {
      id: 0,
      id_cliente: 0,
      cliente: null as any,
      id_vehiculo: 0,
      vehiculo: null as any,
      id_empleado: this.user?.id ?? 0, 
      empleado: null as any,
      fecha_inicio: undefined,
      fecha_fin: undefined,
      costo_total: 0,
      kilometraje_inicial: 0,
      kilometraje_final: 0,
      estado: 'activo'
    };
    setTimeout(() => window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' }), 100);
  }

  saveAlquiler(): void {
    if (!this.selectedAlquiler) return;

    console.log('Guardando alquiler:', this.selectedAlquiler);

    const payload = {
      id_cliente: Number(this.selectedAlquiler.id_cliente),
      id_vehiculo: Number(this.selectedAlquiler.id_vehiculo),
      id_empleado: this.user?.id ?? 0
    };

    this.alquileresService.create(payload as any).subscribe({
      next: () => { /* acción post-creación */ this.newAlquiler(); alert('Alquiler creado con éxito'); },
      error: err => console.error('Error creando alquiler', err)
    });

    this.router.navigate(['/home']);
  }

  cancel(): void {
    this.selectedAlquiler = null;
    this.toDeleteAlquiler = null;
  }
}