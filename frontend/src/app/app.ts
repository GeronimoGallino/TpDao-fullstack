import { HttpClientModule } from '@angular/common/http';
import { Component, signal } from '@angular/core';
import { RouterModule, RouterOutlet } from '@angular/router';
import { Header } from './core/components/header/header';

@Component({
  standalone: true,
  selector: 'app-root',
  imports: [RouterModule, Header, HttpClientModule ],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected readonly title = signal('TP-DAO');
}
