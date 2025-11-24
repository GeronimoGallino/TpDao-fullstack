import { ChangeDetectorRef, Component, ElementRef, OnInit, ViewChild } from '@angular/core';
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
import { forkJoin } from 'rxjs';

@Component({
  selector: 'app-alquileres',
  standalone: true,
  templateUrl: './alquileres.html',
  styleUrls: ['./alquileres.css'],
  imports: [FormsModule, DatePipe, CommonModule]
})
export class AlquileresComponent implements OnInit {

  alquileres: Alquiler[] = [];
  alquileresFiltered: Alquiler[] = [];
  filter = '';

  clientes: Cliente[] = [];
  empleados: Empleado[] = [];
  vehiculos: Vehiculo[] = [];

  selectedAlquiler: Alquiler | null = null;
  toDeleteAlquiler: Alquiler | null = null;
  isEditing = false;
  loading = false;

  kilometrajeFinal: number = 0;

  contratoVisible = false;
  finalizarVisible = false;

  alquilerContrato: Alquiler | null = null;
  alquilerFinalizar: Alquiler | null = null;

  private ctx!: CanvasRenderingContext2D | null;
  private drawing = false;

  @ViewChild('contratoCard') contratoCard!: ElementRef<HTMLDivElement>;
  @ViewChild('firmaCanvas') firmaCanvas!: ElementRef<HTMLCanvasElement>; // Este se mantiene

  constructor(
    private alquileresService: AlquileresService,
    private clientesService: ClientesService,
    private empleadosService: EmpleadosService,
    private vehiculosService: VehiculosService,
    private cdr: ChangeDetectorRef
  ) { }

  ngOnInit(): void {
  this.loading = true;
  forkJoin({
    alquileres: this.alquileresService.getAll(),
    clientes: this.clientesService.getAll(),
    empleados: this.empleadosService.getAll(),
    vehiculos: this.vehiculosService.getAll()
  }).subscribe({
    next: ({ alquileres, clientes, empleados, vehiculos }) => {
      this.alquileres = (alquileres || []).map(a => ({
        ...a,
        fecha_inicio: a.fecha_inicio ? new Date(a.fecha_inicio as any) : new Date()
      }));
      this.clientes = clientes || [];
      this.empleados = empleados || [];
      this.vehiculos = vehiculos || [];
      this.applyFilter();
      this.loading = false;
      this.cdr.markForCheck();
    },
    error: err => {
      console.error('Error cargando datos', err);
      this.loading = false;
      this.cdr.markForCheck();
    }
  });
}


  getEmpleado(id_empleado: number): Empleado | null {
    return this.empleados.find(e => e.id === id_empleado) || null;
  }

  getCliente(id_cliente: number): Cliente | null {
    return this.clientes.find(c => c.id_cliente === id_cliente) || null;
  }

  getVehiculo(id_vehiculo: number): Vehiculo | null {
    return this.vehiculos.find(v => v.id === id_vehiculo) || null;
  }


  verContrato(a: Alquiler): void {
    this.alquilerContrato = a;
    this.contratoVisible = true;
    this.finalizarVisible = false;

    // Espera a que el modal renderice el canvas
    setTimeout(() => this.initCanvas(), 50);
  }

  finalizarContrato(a: Alquiler): void {
    this.finalizarVisible = true;
    this.contratoVisible = false;
    this.alquilerFinalizar = a;
  }

  private initCanvas() {
    if (!this.firmaCanvas) return;

    const canvas = this.firmaCanvas.nativeElement;
    this.ctx = canvas.getContext('2d');

    if (!this.ctx) return;

    this.ctx.lineWidth = 2;
    this.ctx.lineCap = 'round';
  }

  // === Firma en Canvas === //

  startDraw(e: MouseEvent) {
    if (!this.ctx) return;

    this.drawing = true;

    const rect = this.firmaCanvas.nativeElement.getBoundingClientRect();
    this.ctx.beginPath();
    this.ctx.moveTo(e.clientX - rect.left, e.clientY - rect.top);
  }

  draw(e: MouseEvent) {
    if (!this.drawing || !this.ctx) return;

    const rect = this.firmaCanvas.nativeElement.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    this.ctx.lineTo(x, y);
    this.ctx.stroke();
  }

  endDraw() {
    this.drawing = false;
    if (this.ctx) this.ctx.beginPath();
  }

  // === Descargar contrato === //

  descargarContrato() {
    // 1. Verificar si el contenedor del contrato está disponible
    if (!this.contratoCard) return;

    // 2. Clonar el contenido de la tarjeta del contrato (para no modificar el original visible)
    const printContent = this.contratoCard.nativeElement.cloneNode(true) as HTMLDivElement;

    // 3. Eliminar los botones y elementos de control del modal para que no aparezcan en la impresión
    printContent.querySelector('.cerrar')?.remove();
    printContent.querySelector('button:last-child')?.remove(); // El botón de "Descargar"

    // 4. Obtener la imagen Base64 de la firma dibujada en el canvas
    const firmaBase64 = this.firmaCanvas.nativeElement.toDataURL();

    // 5. Crear un elemento de imagen HTML y configurarlo
    const imgFirma = document.createElement('img');
    imgFirma.src = firmaBase64;
    imgFirma.width = 400;
    imgFirma.style.border = '1px solid #000';
    imgFirma.style.marginTop = '10px';

    // 6. Reemplazar el elemento <canvas> por la imagen de la firma
    const canvasElement = printContent.querySelector('canvas');
    if (canvasElement) {
      const parent = canvasElement.parentElement;
      if (parent) {
        parent.replaceChild(imgFirma, canvasElement);
      }
    }

    // 7. Obtener el HTML final del contenido del contrato
    const htmlContent = printContent.outerHTML;

    // 8. Abrir ventana de impresión
    const win = window.open('', '_blank');

    // Escribimos la estructura de la página de impresión con estilos básicos para el contrato
    win!.document.write(`
      <html>
        <head>
            <title>Contrato de Arrendamiento de Vehículo</title>
            <style>
                body { font-family: Arial, sans-serif; padding: 20px; }
                .contrato-card { max-width: 800px; margin: 0 auto; padding: 20px; }
                h2 { text-align: center; }
                p { margin: 10px 0; line-height: 1.5; text-align: justify; }
                strong { font-weight: bold; }
                table { width: 100%; border: none; text-align: center; margin-top: 40px; }
                table td div { border-top: 1px solid #000; padding-top: 5px; }
                img { display: block; margin: 10px 0; }
            </style>
        </head>
        <body>
            ${htmlContent}
        </body>
      </html>
    `);

    win!.document.close();
    win!.print();
  }

  cerrarContrato(): void {
    this.contratoVisible = false;
    this.alquilerContrato = null;
  }

  confirmarFinalizacion() {
    console.log('Finalizando contrato...');
    if (this.alquilerFinalizar === null || this.kilometrajeFinal < this.alquilerFinalizar?.kilometraje_inicial) {
      alert('El kilometraje final no puede ser menor que el kilometraje inicial.');
    }

  }

  cerrarFinalizar() {
    this.finalizarVisible = false;
  }

  // === Servicios === //

  loadAlquileres(): void {
    this.loading = true;
    this.alquileresService.getAll().subscribe({
      next: list => {
        this.alquileres = (list || []).map(a => ({
          ...a,
          fecha_inicio: a.fecha_inicio ? new Date(a.fecha_inicio as any) : new Date()
        }));

        this.cdr.markForCheck();
        this.applyFilter();
        this.loading = false;
      },
      error: err => {
        console.error('Error cargando alquileres', err);
        this.cdr.markForCheck();
        this.loading = false;
      }
    });
  }

  loadClientes(): void {
    this.clientesService.getAll().subscribe({
      next: list => this.clientes = list || [],
      error: err => console.error('Error cargando clientes', err)
    });
  }

  loadEmpleados(): void {
    this.empleadosService.getAll().subscribe({
      next: list => this.empleados = list || [],
      error: err => console.error('Error cargando empleados', err)
    });
  }

  loadVehiculos(): void {
    this.vehiculosService.getAll().subscribe({
      next: list => this.vehiculos = list || [],
      error: err => console.error('Error cargando vehículos', err)
    });
  }

  // === Filtro === //

  applyFilter(): void {
    const q = (this.filter || '').toLowerCase().trim();
    if (!q) {
      this.alquileresFiltered = [...this.alquileres];
      return;
    }
    this.alquileresFiltered = this.alquileres.filter(a =>
      (a.cliente?.nombre || '').toLowerCase().includes(q) ||
      (a.vehiculo?.marca || '').toLowerCase().includes(q) ||
      (a.vehiculo?.modelo || '').toLowerCase().includes(q) ||
      (a.estado || '').toLowerCase().includes(q)
    );
  }

  // === CRUD === //

  newAlquiler(): void {
    this.selectedAlquiler = {
      id_alquiler: 0,
      id_cliente: 0,
      cliente: null as any,
      id_vehiculo: 0,
      vehiculo: null as any,
      id_empleado: 1, // cambiar despues cuando usemos sesionessssssss -----------------------------------
      empleado: null as any,
      fecha_inicio: new Date(),
      kilometraje_inicial: 0,
      estado: 'activo'
    };
    this.isEditing = false;
    setTimeout(() => window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' }), 100);
  }

  editAlquiler(a: Alquiler): void {
    this.selectedAlquiler = {
      ...a,
      fecha_inicio: undefined
    };
    this.isEditing = true;
    setTimeout(() => window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' }), 100);
  }

  saveAlquiler(): void {
    if (!this.selectedAlquiler) return;

    const payload = { ...this.selectedAlquiler, id_empleado: 1 }; // cambiar despues cuando usemos sesionessssssss -----------------------------------

    if (this.isEditing) {
      this.alquileresService.update(payload).subscribe({
        next: () => { this.loadAlquileres(); this.cancel(); },
        error: err => console.error('Error actualizando alquiler', err)
      });
    } else {
      this.alquileresService.create(payload).subscribe({
        next: () => { this.loadAlquileres(); this.cancel(); },
        error: err => console.error('Error creando alquiler', err)
      });
    }
  }


  confirmDelete(a: Alquiler): void {
    this.toDeleteAlquiler = a;
  }

  deleteAlquiler(a?: Alquiler): void {
    const target = a ?? this.toDeleteAlquiler;
    if (!target) return;
    this.alquileresService.delete(target.id_alquiler).subscribe({
      next: () => { this.toDeleteAlquiler = null; this.loadAlquileres(); },
      error: err => console.error('Error eliminando alquiler', err)
    });
  }

  cancel(): void {
    this.selectedAlquiler = null;
    this.toDeleteAlquiler = null;
    this.isEditing = false;
  }
}
