import { ChangeDetectionStrategy, ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { Cliente } from '../../core/interfaces/cliente';
import { ClientesService } from '../../core/services/clientes-service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-clientes',
  templateUrl: './clientes.html',
  styleUrls: ['./clientes.css'],
  standalone: true,
  imports: [CommonModule, FormsModule],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class ClientesComponent implements OnInit {
  clientes: Cliente[] = [];
  clientesFiltered: Cliente[] = [];
  filter: string = '';

  selectedCliente: Cliente | null = null;
  toDeleteCliente: Cliente | null = null;
  isEditing = false;
  loading = false;

  constructor(
    private clientesService: ClientesService,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit(): void {
    this.applyFilter();
    this.loadClientes();
  }

  loadClientes(): void {
    this.loading = true;
    this.clientesService.getAll().subscribe({
      next: list => {
        this.clientes = list || [];
        this.applyFilter();

        this.cdr.markForCheck(); // fuerza actualización para OnPush

        this.loading = false;
      },
      error: err => {
        console.error('Error cargando clientes', err);
        this.loading = false;
        this.cdr.markForCheck();
      }
    });
  }

  applyFilter(): void {
    const q = (this.filter || '').toLowerCase().trim();
    if (!q) {
      this.clientesFiltered = [...this.clientes];
      return;
    }
    this.clientesFiltered = this.clientes.filter(c =>
      (c.nombre || '').toLowerCase().includes(q) ||
      (c.dni || '').toLowerCase().includes(q)
    );
  }

  newCliente(): void {
    this.selectedCliente = {
      id_cliente: 0,
      nombre: '',
      dni: '',
      telefono: '',
      email: '',
      direccion: '',
      fecha_registro: new Date()
    };
    this.isEditing = false;
    setTimeout(() => window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' }), 100);
  }

  editCliente(c: Cliente): void {
    this.selectedCliente = { ...c, fecha_registro: c.fecha_registro ? new Date(c.fecha_registro) : new Date() };
    this.isEditing = true;
    setTimeout(() => window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' }), 100);
  }

  saveCliente(): void {
    if (!this.selectedCliente) return;

    if (this.isEditing) {
      this.clientesService.update(this.selectedCliente).subscribe({
        next: () => {
          this.loadClientes();
          this.cancel();
        },
        error: err => console.error('Error actualizando cliente', err)
      });
    } else {
      this.clientesService.create(this.selectedCliente).subscribe({
        next: () => {
          this.loadClientes();
          this.cancel();
        },
        error: err => console.error('Error creando cliente', err)
      });
    }
  }

  confirmDelete(c: Cliente): void {
    this.toDeleteCliente = c;
  }

  deleteCliente(c?: Cliente): void {
    const target = c ?? this.toDeleteCliente;
    if (!target) return;

    this.clientesService.delete(target.id_cliente).subscribe({
      next: () => {
        this.toDeleteCliente = null;
        this.loadClientes();
      },
      error: err => console.error('Error eliminando cliente', err)
    });
  }

  cancel(): void {
    this.selectedCliente = null;
    this.toDeleteCliente = null;
    this.isEditing = false;
  }
}
