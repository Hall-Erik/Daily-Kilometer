import { NgModule } from '@angular/core';

import { MatToolbarModule } from '@angular/material/toolbar';
import { MatButtonModule } from '@angular/material/button'; 
import { MatMenuModule } from '@angular/material/menu'; 
import { MatDividerModule } from '@angular/material/divider'; 
import { MatIconModule } from '@angular/material/icon'; 
import { MatCardModule } from '@angular/material/card'; 
import { MatListModule } from '@angular/material/list';

const material = [
  MatToolbarModule,
  MatButtonModule,
  MatMenuModule,
  MatDividerModule,
  MatIconModule,
  MatCardModule,
  MatListModule
];

@NgModule({
  imports: [material],
  exports: [material]
})
export class MaterialModule { }
