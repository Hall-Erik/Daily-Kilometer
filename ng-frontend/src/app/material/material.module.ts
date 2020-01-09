import { NgModule } from '@angular/core';

import {MatToolbarModule} from '@angular/material/toolbar';

const material = [
  MatToolbarModule
];

@NgModule({
  imports: [material],
  exports: [material]
})
export class MaterialModule { }
