import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { Empleado } from '../../core/interfaces/empleado';
import { EmpleadosService } from '../../core/services/empleados-service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-empleados',
  templateUrl: './empleados.html',
  styleUrls: ['./empleados.css'],
  standalone: true,
  imports: [CommonModule, FormsModule] 
})
export class EmpleadosComponent implements OnInit {
  empleados: Empleado[] = [];
  empleadosFiltered: Empleado[] = [];
  filter = '';

  selectedEmpleado: Empleado | null = null;
  toDeleteEmpleado: Empleado | null = null;
  isEditing = false;
  loading = false;

  // NUEVO: mensaje de error del backend
  errorMessage: string | null = null;

  constructor(private empleadosService: EmpleadosService,
              private cdr: ChangeDetectorRef) {}

  ngOnInit(): void {
    this.applyFilter();
    this.loadEmpleados();
  }

  loadEmpleados(): void {
    this.loading = true;
    this.empleadosService.getAll().subscribe({
      next: list => {
        this.empleados = list || [];
        this.applyFilter();
        this.cdr.markForCheck();
        this.loading = false;
      },
      error: err => {
        console.error('Error cargando empleados', err);
        this.cdr.markForCheck();
        this.loading = false;
      }
    });
  }

  applyFilter(): void {
    const q = (this.filter || '').toLowerCase().trim();
    if (!q) {
      this.empleadosFiltered = [...this.empleados];
      return;
    }
    this.empleadosFiltered = this.empleados.filter(e =>
      (e.nombre || '').toLowerCase().includes(q) ||
      (e.dni || '').toLowerCase().includes(q) ||
      (e.cargo || '').toLowerCase().includes(q)
    );
  }

  newEmpleado(): void {
    this.selectedEmpleado = {
      id: 0,
      nombre: '',
      dni: '',
      cargo: '',
      telefono: '',
      email: '',
      fecha_inicio: new Date(),
      id_negocio: 0,
      negocio: null as any
    };
    this.isEditing = false;
    this.errorMessage = null;
    setTimeout(() => window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' }), 100);
  }

  editEmpleado(e: Empleado): void {
    this.selectedEmpleado = { ...e, fecha_inicio: e.fecha_inicio ? new Date(e.fecha_inicio) : new Date() };
    this.isEditing = true;
    this.errorMessage = null;
    setTimeout(() => window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' }), 100);
  }

  saveEmpleado(): void {
    if (!this.selectedEmpleado) return;

    this.errorMessage = null;

    if (this.isEditing) {
      this.empleadosService.update(this.selectedEmpleado).subscribe({
        next: () => { this.loadEmpleados(); this.cancel(); },
        error: err => {
          this.errorMessage = err.error?.detail || 'Error actualizando empleado';
          this.cdr.markForCheck();
        }
      });
    } else {
      this.empleadosService.create(this.selectedEmpleado).subscribe({
        next: () => { this.loadEmpleados(); this.cancel(); },
        error: err => {
          this.errorMessage = err.error?.detail || 'Error creando empleado';
          this.cdr.markForCheck();
        }
      });
    }
  }

  confirmDelete(e: Empleado): void {
    this.toDeleteEmpleado = e;
  }

  deleteEmpleado(e?: Empleado): void {
    const target = e ?? this.toDeleteEmpleado;
    if (!target) return;
    this.empleadosService.delete(target.id).subscribe({
      next: () => { this.toDeleteEmpleado = null; this.loadEmpleados(); },
      error: err => console.error('Error eliminando empleado', err)
    });
  }

  cancel(): void {
    this.selectedEmpleado = null;
    this.toDeleteEmpleado = null;
    this.isEditing = false;
    this.errorMessage = null;
  }

  // NUEVO: permite solo números en DNI y teléfono
  allowOnlyNumbers(event: KeyboardEvent) {
    const charCode = event.which ? event.which : event.keyCode;
    if (charCode > 31 && (charCode < 48 || charCode > 57)) {
      event.preventDefault();
    }
  }
}
