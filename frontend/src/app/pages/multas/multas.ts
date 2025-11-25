import { ChangeDetectionStrategy, ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { Multa } from '../../core/interfaces/multa';
import { MultasService } from '../../core/services/multas-service';
import { AlquileresService } from '../../core/services/alquileres-service';
import { VehiculosService } from '../../core/services/vehiculos-service';
import { ClientesService } from '../../core/services/clientes-service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Cliente } from '../../core/interfaces/cliente';
import { Vehiculo } from '../../core/interfaces/vehiculo';
import { Alquiler } from '../../core/interfaces/alquiler';
import { forkJoin } from 'rxjs';

@Component({
  selector: 'app-multas',
  templateUrl: './multas.html',
  styleUrls: ['./multas.css'],
  standalone: true,
  imports: [CommonModule, FormsModule],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class MultasComponent implements OnInit {
  multas: Multa[] = [];
  multasFiltered: Multa[] = [];
  filter: string = '';

  selectedMulta: Multa | null = null;
  toDeleteMulta: Multa | null = null;
  isEditing = false;
  loading = false;

  alquileres: any[] = [];
  vehiculos: any[] = [];
  clientes: any[] = [];

  constructor(
    private multasService: MultasService,
    private alquileresService: AlquileresService,
    private vehiculosService: VehiculosService,
    private clientesService: ClientesService,
    private cdr: ChangeDetectorRef
  ) { }

  alquileresOptions: { id_alquiler: number, display: string }[] = [];

  ngOnInit(): void {
    // forkJoin como antes
    forkJoin({
      alquileres: this.alquileresService.getAll(),
      vehiculos: this.vehiculosService.getAll(),
      clientes: this.clientesService.getAll()
    }).subscribe({
      next: ({ alquileres, vehiculos, clientes }) => {
        this.alquileres = (alquileres || []).filter(a => a.estado === "Activo");;
        this.vehiculos = vehiculos || [];
        this.clientes = clientes || [];

        // Generamos las opciones del select
        this.alquileresOptions = this.alquileres.map(a => {
          const cliente = this.getCliente(a.id_cliente ?? 0);
          const vehiculo = this.getVehiculo(a.id_vehiculo ?? 0);

          return {
            id_alquiler: a.id,
            display: `${cliente?.nombre ?? 'N/A'} - (${vehiculo?.marca ?? ''} ${vehiculo?.modelo ?? ''})`
          };
        });
        console.log(this.alquileresOptions);
        this.loadMultas();
        this.cdr.markForCheck();
      },
      error: err => console.error('Error cargando datos de referencia', err)
    });
  }


  testDisplay(): void {
    console.log('--- Probando getCliente y getVehiculo ---');
    this.alquileres.forEach(a => {
      const cliente = this.getCliente(a?.id_cliente ?? 0);
      const vehiculo = this.getVehiculo(a?.id_vehiculo ?? 0);

      console.log(
        `Multa: ${a.descripcion}, Cliente: ${cliente?.nombre ?? 'N/A'}, Vehículo: ${vehiculo?.marca ?? ''} ${vehiculo?.modelo ?? ''}`
      );
    });
  }

  getCliente(id_cliente: number): Cliente | null {
    return this.clientes.find(c => c.id_cliente === id_cliente) || null;
  }

  getVehiculo(id_vehiculo: number): Vehiculo | null {
    return this.vehiculos.find(v => v.id === id_vehiculo) || null;
  }

  getAlquiler(id_alquiler: number): Alquiler | null {
    return this.vehiculos.find(v => v.id === id_alquiler) || null;
  }

  loadMultas(): void {
    this.loading = true;
    this.multasService.getAll().subscribe({
      next: list => {
        this.multas = list || [];
        this.applyFilter();
        this.cdr.markForCheck();
        this.loading = false;
      },
      error: err => {
        console.error('Error cargando multas', err);
        this.loading = false;
        this.cdr.markForCheck();
      }
    });
  }

  loadAlquileres(): void {
    this.alquileresService.getAll().subscribe({
      next: list => {
        this.alquileres = list || [];
        this.cdr.markForCheck();
      },
      error: err => console.error('Error cargando alquileres', err)
    });
  }

  loadVehiculos(): void {
    this.vehiculosService.getAll().subscribe({
      next: list => {
        this.vehiculos = list || [];
        this.cdr.markForCheck();
      },
      error: err => console.error('Error cargando vehículos', err)
    });
  }

  loadClientes(): void {
    this.clientesService.getAll().subscribe({
      next: list => {
        this.clientes = list || [];
        this.cdr.markForCheck();
      },
      error: err => console.error('Error cargando clientes', err)
    });
  }

  applyFilter(): void {
    const q = (this.filter || '').toLowerCase().trim();
    if (!q) {
      this.multasFiltered = [...this.multas];
      return;
    }
    this.multasFiltered = this.multas.filter(m =>
      (m.tipo || '').toLowerCase().includes(q) ||
      (m.descripcion || '').toLowerCase().includes(q)
    );
  }

  newMulta(): void {
    this.selectedMulta = {
      id_alquiler: 0,
      tipo: '',
      descripcion: '',
      costo: 0,
      fecha: new Date()
    };
    this.isEditing = false;
    setTimeout(() => window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' }), 100);
  }

  editMulta(m: Multa): void {
    this.selectedMulta = { ...m, fecha: m.fecha ? new Date(m.fecha) : new Date() };
    this.isEditing = true;
    setTimeout(() => window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' }), 100);
  }

  saveMulta(): void {
    if (!this.selectedMulta) return;
    const obs$ = this.isEditing
      ? this.multasService.update(this.selectedMulta)
      : this.multasService.create(this.selectedMulta);


    obs$.subscribe({
      next: () => {
        this.loadMultas();
        this.cancel();
      },
      error: err => console.error('Error guardando multa', err)
    });


  }

  confirmDelete(m: Multa): void {
    this.toDeleteMulta = m;
  }

  deleteMulta(m?: Multa): void {
    const target = m ?? this.toDeleteMulta;
    if (!target) return;
    this.multasService.delete(target.id_alquiler).subscribe({
      next: () => {
        this.toDeleteMulta = null;
        this.loadMultas();
      },
      error: err => console.error('Error eliminando multa', err)
    });
  }

  cancel(): void {
    this.selectedMulta = null;
    this.toDeleteMulta = null;
    this.isEditing = false;
  }

  trackById(index: number, item: Multa) {
    return item.id_alquiler + '-' + item.fecha;
  }
}
