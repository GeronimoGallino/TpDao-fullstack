import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MantService } from '../../core/services/mant-service';
import { Mantenimiento } from '../../core/interfaces/mantenimiento';
import { Vehiculo } from '../../core/interfaces/vehiculo';
import { VehiculosService } from '../../core/services/vehiculos-service';
import { Router } from '@angular/router';
import { AuthService } from '../../core/services/auth-service';
import { User } from '../../core/interfaces/user';

@Component({
  selector: 'app-mant-nuevo',
  templateUrl: './mant-nuevo.html',
  styleUrls: ['./mant-nuevo.css'],
  standalone: true,
  imports: [CommonModule, FormsModule]
})
export class MantenimientosComponent {

  loading = false;
  vehiculos: Vehiculo[] = [];
  user: User | null = null;
  mantenimiento: Mantenimiento;

  constructor(
    private mantService: MantService,
    private vehiculosService: VehiculosService,
    private router: Router,
    private authService: AuthService
  ) {
    // Inicializamos mantenimiento vacío; id_empleado se asigna en ngOnInit
    this.mantenimiento = {} as Mantenimiento;
  }

  ngOnInit(): void {
    this.loadVehiculos();
    this.user = this.authService.getCurrentUser();
    this.resetMantenimiento(); // inicializamos el modelo con id_empleado
  }

  // Función para crear o resetear el modelo
  resetMantenimiento(): void {
    this.mantenimiento = {
      id_vehiculo: 0,
      id_empleado: this.user?.id ?? 0, // asignamos el empleado logueado
      km_actual: 0,
      tipo: 'preventivo',
      costo: 0,
      observaciones: '',
      id_mantenimiento: 0,
      vehiculo: undefined,
      empleado: undefined
    };
  }

  loadVehiculos(): void {
    this.vehiculosService.getAllActive().subscribe({
      next: list => this.vehiculos = list || [],
      error: err => console.error(err)
    });
  }

  onVehiculoChange(id_vehiculo: Number) {
    const id = Number(id_vehiculo);
    const vehiculoSeleccionado = this.vehiculos.find(v => v.id === id);
    if (vehiculoSeleccionado) {
      this.mantenimiento.km_actual = vehiculoSeleccionado.kilometraje ?? 0;
    } else {
      this.mantenimiento.km_actual = 0;
    }
  }

  crearMantenimiento(): void {
    this.loading = true;
    console.log(this.mantenimiento);

    this.mantService.create(this.mantenimiento).subscribe({
      next: (resp) => {
        console.log('Mantenimiento creado:', resp);

        // Reseteo del formulario, mantiene id_empleado
        this.resetMantenimiento();

        alert('Mantenimiento creado con éxito!');
        this.router.navigate(['/home']);
        this.loading = false;
      },
      error: (err) => {
        console.error('Error creando mantenimiento:', err);
        this.loading = false;
      }
    });

  }
}
