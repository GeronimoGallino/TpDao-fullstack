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

  constructor(private empleadosService: EmpleadosService,
    private cdr: ChangeDetectorRef
  ) {}

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
      id_empleado: 0,
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
    setTimeout(() => window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' }), 100);
  }

  editEmpleado(e: Empleado): void {
    this.selectedEmpleado = { ...e, fecha_inicio: e.fecha_inicio ? new Date(e.fecha_inicio) : new Date() };
    this.isEditing = true;
    setTimeout(() => window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' }), 100);
  }

  saveEmpleado(): void {
    if (!this.selectedEmpleado) return;

    if (this.isEditing) {
      this.empleadosService.update(this.selectedEmpleado).subscribe({
        next: () => { this.loadEmpleados(); this.cancel(); },
        error: err => console.error('Error actualizando empleado', err)
      });
    } else {
      this.empleadosService.create(this.selectedEmpleado).subscribe({
        next: () => { this.loadEmpleados(); this.cancel(); },
        error: err => console.error('Error creando empleado', err)
      });
    }
  }

  confirmDelete(e: Empleado): void {
    this.toDeleteEmpleado = e;
  }

  deleteEmpleado(e?: Empleado): void {
    const target = e ?? this.toDeleteEmpleado;
    if (!target) return;
    this.empleadosService.delete(target.id_empleado).subscribe({
      next: () => { this.toDeleteEmpleado = null; this.loadEmpleados(); },
      error: err => console.error('Error eliminando empleado', err)
    });
  }

  cancel(): void {
    this.selectedEmpleado = null;
    this.toDeleteEmpleado = null;
    this.isEditing = false;
  }
}