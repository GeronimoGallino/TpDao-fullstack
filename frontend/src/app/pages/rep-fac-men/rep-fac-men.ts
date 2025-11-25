import { Component, OnInit, ChangeDetectionStrategy, inject, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { finalize } from 'rxjs/operators';
import { RepFacMen } from '../../core/services/rep-fac-men';

interface FacturacionMensual {
  mes: string;
  total: number;
}

@Component({
  selector: 'app-rep-fac-men',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './rep-fac-men.html',
  styleUrls: ['./rep-fac-men.css'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class RepFacMenComponent implements OnInit {
  datos: FacturacionMensual[] = [];
  loading = true;
  error = '';
  maxTotal = 1;

  private repFacMenService = inject(RepFacMen);
  private cdr = inject(ChangeDetectorRef);

  ngOnInit(): void {
    console.log('RepFacMenComponent: iniciando carga de datos');
    this.repFacMenService.getFacMensual()
      .pipe(
        finalize(() => {
          this.loading = false;
          this.cdr.markForCheck();
          console.log('RepFacMenComponent: finalize -> loading false');
        })
      )
      .subscribe({
        next: (res: FacturacionMensual[]) => {
          console.log('RepFacMenComponent: datos recibidos', res);
          // Mostrar de más antiguo a más reciente:
          this.datos = res.slice().reverse();
          this.maxTotal = Math.max(1, ...this.datos.map(d => d.total));
          this.cdr.markForCheck();
        },
        error: (err) => {
          console.error('RepFacMenComponent: error al cargar facturación mensual', err);
          this.error = err?.message || 'Error al cargar datos';
          this.cdr.markForCheck();
        }
      });
  }

  getHeight(total: number): number {
    if (total <= 0) return 0.8; // mínima visibilidad
    return (total / this.maxTotal) * 100;
  }

  getMesLabel(mes: string): string {
    const parts = mes.split('-');
    if (parts.length !== 2) return mes;
    const year = Number(parts[0]);
    const monthIndex = Number(parts[1]) - 1;
    const date = new Date(year, monthIndex, 1);
    const month = date.toLocaleString('es-AR', { month: 'short' }).replace('.', '');
    const yearShort = date.toLocaleString('es-AR', { year: '2-digit' });
    return `${month.charAt(0).toUpperCase() + month.slice(1)} '${yearShort}`;
  }

  trackByMes(index: number, item: FacturacionMensual): string {
    return item.mes;
  }
}