import { Component, OnInit } from '@angular/core';
import { CommonModule, DatePipe, DecimalPipe } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RepAlqPerService } from '../../core/services/rep-alq-per';
import { forkJoin } from 'rxjs';

@Component({
  selector: 'app-rep-alq-per',
  standalone: true,
  templateUrl: './rep-alq-per.html',
  styleUrl: './rep-alq-per.css',
  imports: [CommonModule, FormsModule],
  providers: [DatePipe, DecimalPipe]
})
export class RepAlqPer implements OnInit {

  tipo: string = 'anual';
  anio: number | any = null;
  valor: number | any = null;

  anios: number[] = [];
  meses: any[] = [];
  trimestres: any[] = [];

  respuesta: any = null;
  loading: boolean = false;
  error: string | null = null;

  totalCosto: number = 0;

  constructor(private repAlqPerService: RepAlqPerService) { }

  ngOnInit(): void {
    this.generarAnios();
    this.generarMeses();
    this.generarTrimestres();
    this.anio = new Date().getFullYear();
    this.loadReporte();
  }

  generarAnios(): void {
    const actual = new Date().getFullYear();
    for (let y = actual; y >= actual - 8; y--) {
      this.anios.push(y);
    }
  }

  generarMeses(): void {
    this.meses = [
      { value: 1, label: '1 - Enero' },
      { value: 2, label: '2 - Febrero' },
      { value: 3, label: '3 - Marzo' },
      { value: 4, label: '4 - Abril' },
      { value: 5, label: '5 - Mayo' },
      { value: 6, label: '6 - Junio' },
      { value: 7, label: '7 - Julio' },
      { value: 8, label: '8 - Agosto' },
      { value: 9, label: '9 - Septiembre' },
      { value: 10, label: '10 - Octubre' },
      { value: 11, label: '11 - Noviembre' },
      { value: 12, label: '12 - Diciembre' }
    ];
  }

  generarTrimestres(): void {
    this.trimestres = [
      { value: 1, label: '1 → Ene - Mar' },
      { value: 2, label: '2 → Abr - Jun' },
      { value: 3, label: '3 → Jul - Sep' },
      { value: 4, label: '4 → Oct - Dic' }
    ];
  }

  onTipoChange(): void {
    if (this.tipo === 'mensual') {
      this.valor = 1; // primer mes por defecto
    } else if (this.tipo === 'trimestral') {
      this.valor = 1; // primer trimestre por defecto
    } else {
      this.valor = null; // anual no necesita valor
    }
    this.loadReporte();
  }


  onAnioChange(): void {
    this.loadReporte();
  }

  onValorChange(): void {
    this.loadReporte();
  }

  loadReporte(): void {
    this.error = null;
    this.respuesta = null;
    this.totalCosto = 0;


    if (!this.tipo || !this.anio) {
      this.error = 'Seleccione tipo y año.';
      return;
    }

    if (this.tipo === 'mensual' && (!this.valor || this.valor < 1 || this.valor > 12)) {
      this.error = 'Seleccione un mes válido.';
      return;
    }

    if (this.tipo === 'trimestral' && (!this.valor || this.valor < 1 || this.valor > 4)) {
      this.error = 'Seleccione un trimestre válido.';
      return;
    }

    this.loading = true;

    this.repAlqPerService.getReporte(this.tipo, this.anio, this.valor).subscribe({
      next: data => {
        this.respuesta = data || null;
        if (data && data.alquileres) {
          this.totalCosto = data.alquileres.reduce((acc: number, alq: any) => acc + (alq.costo_total || 0), 0);
        }
        this.loading = false;
      },
      error: err => {
        console.error(err);
        this.error = 'Error al generar el reporte.';
        this.loading = false;
      }
    });

  }

  trackById(index: number, item: any) {
    return item.fecha_inicio + '-' + item.fecha_fin;
  }
}
