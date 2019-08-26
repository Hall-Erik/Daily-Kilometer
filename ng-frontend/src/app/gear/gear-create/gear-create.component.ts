import { Component } from '@angular/core';
import { Router } from '@angular/router';

import { GearService } from '../../services/gear.service';

import { Gear } from '../../models/gear';

@Component({
  selector: 'app-gear-create',
  templateUrl: './gear-create.component.html',
  styleUrls: ['./gear-create.component.css']
})
export class GearCreateComponent {

  constructor(private gearService: GearService,
              private router: Router) { }

  submit(gear: Gear) {
    this.gearService.create_gear(gear).subscribe(() => {
      this.router.navigate(['gear']);
    });
  }
}
