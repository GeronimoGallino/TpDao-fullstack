import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { CommonModule, NgFor, NgIf } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Vehiculo } from '../../core/interfaces/vehiculo';
import { VehiculosService } from '../../core/services/vehiculos-service';

@Component({
  selector: 'app-vehiculos',
  templateUrl: './vehiculos.html',
  styleUrls: ['./vehiculos.css'],
  standalone: true,
  imports: [CommonModule, FormsModule, NgIf, NgFor]  
})
export class VehiculosComponent implements OnInit {
  vehiculos: Vehiculo[] = [];
  vehiculosFiltered: Vehiculo[] = [];
  filter = '';

  selectedVehiculo: Vehiculo | null = null;
  toDeleteVehiculo: Vehiculo | null = null;
  isEditing = false;
  loading = false;
  errorMessage: string | null = null; // <-- para mostrar errores de patente duplicada

  constructor(private vehiculosService: VehiculosService,
              private cdr: ChangeDetectorRef) {}

  ngOnInit(): void {
    this.applyFilter();
    this.loadVehiculos();
  }

  loadVehiculos(): void {
    this.loading = true;
    this.vehiculosService.getAll().subscribe({
      next: list => {
        this.vehiculos = list || [];
        this.applyFilter();
        this.cdr.markForCheck();
        this.loading = false;
      },
      error: err => {
        console.error('Error cargando vehículos', err);
        this.cdr.markForCheck();
        this.loading = false;
      }
    });
  }

  applyFilter(): void {
    const q = (this.filter || '').toLowerCase().trim();
    if (!q) {
      this.vehiculosFiltered = [...this.vehiculos];
      return;
    }
    this.vehiculosFiltered = this.vehiculos.filter(v =>
      (v.marca || '').toLowerCase().includes(q) ||
      (v.modelo || '').toLowerCase().includes(q) ||
      (v.anio || '').toString().includes(q) ||
      (v.patente || '').toLowerCase().includes(q) ||
      (v.tipo || '').toLowerCase().includes(q) ||
      (v.kilometraje || '').toString().includes(q) ||
      (v.costo_diario || '').toString().includes(q) ||
      (v.estado || '').toLowerCase().includes(q)
    );
  }

  newVehiculo(): void {
    this.selectedVehiculo = {
      id: 0,
      marca: '',
      modelo: '',
      anio: new Date().getFullYear(),
      patente: '',
      tipo: '',
      kilometraje: 0,
      disponible: true,
      costo_diario: 0,
      estado: ''
    };
    this.isEditing = false;
    this.errorMessage = null;
    setTimeout(() => window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' }), 100);
  }

  editVehiculo(v: Vehiculo): void {
    this.selectedVehiculo = { ...v };
    this.isEditing = true;
    this.errorMessage = null;
    setTimeout(() => window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' }), 100);
  }

  saveVehiculo(): void {
  if (!this.selectedVehiculo) return;

  this.errorMessage = null; // limpiar error previo

  const obs = this.isEditing 
    ? this.vehiculosService.update(this.selectedVehiculo)
    : this.vehiculosService.create(this.selectedVehiculo);

  obs.subscribe({
    next: () => { this.loadVehiculos(); this.cancel(); },
    error: err => {
      console.error('Error creando/actualizando vehículo', err);
      this.errorMessage = this.extractErrorMessage(err);
      this.cdr.markForCheck(); // <- IMPORTANTE
    }
  });
}

  // Extrae el mensaje de error enviado desde el backend
  private extractErrorMessage(err: any): string {
    if (err.error && typeof err.error.detail === 'string') {
      return err.error.detail;
    }
    return 'Ocurrió un error inesperado';
  }

  confirmDelete(v: Vehiculo): void {
    this.toDeleteVehiculo = v;
  }

  deleteVehiculo(v?: Vehiculo): void {
    const target = v ?? this.toDeleteVehiculo;
    if (!target) return;
    this.vehiculosService.delete(target.id).subscribe({
      next: () => { this.toDeleteVehiculo = null; this.loadVehiculos(); },
      error: err => console.error('Error eliminando vehículo', err)
    });
  }

  cancel(): void {
    this.selectedVehiculo = null;
    this.toDeleteVehiculo = null;
    this.isEditing = false;
    this.errorMessage = null;
  }
}
