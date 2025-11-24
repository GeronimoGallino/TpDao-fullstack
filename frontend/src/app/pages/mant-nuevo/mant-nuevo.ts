import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MantService } from '../../core/services/mant-service';
import { Mantenimiento } from '../../core/interfaces/mantenimiento';
import { Vehiculo } from '../../core/interfaces/vehiculo';
import { VehiculosService } from '../../core/services/vehiculos-service';

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

  ngOnInit(): void {
    this.loadVehiculos();
  }

  // Acá va tu modelo, inicializado
  mantenimiento: Mantenimiento = {
    id_vehiculo: 0,
    id_empleado: 1, // cambiar con las sesionessssss -------------------------
    fecha: '',
    km_actual: 0,
    tipo: 'preventivo',
    costo: 0,
    observaciones: '', 
    id_mantenimiento: 0,
    vehiculo: undefined,
    empleado: undefined
  };

  constructor(private mantService: MantService,
    private vehiculosService: VehiculosService) { }

  loadVehiculos(): void {
    this.vehiculosService.getAllActive().subscribe({ next: list => this.vehiculos = list || [], error: err => console.error(err) });
  }

  crearMantenimiento(): void {
    this.loading = true;

    this.mantService.create(this.mantenimiento).subscribe({
      next: (resp) => {
        console.log('Mantenimiento creado:', resp);

        // Reseteo del formulario
        this.mantenimiento = {
          id_vehiculo: 0,
          id_empleado: 0,
          fecha: '',
          km_actual: 0,
          tipo: 'preventivo',
          costo: 0,
          observaciones: '',
          empleado: undefined,
          vehiculo: undefined
        };

        this.loading = false;
      },
      error: (err) => {
        console.error('Error creando mantenimiento:', err);
        this.loading = false;
      }
    });
  }
}
