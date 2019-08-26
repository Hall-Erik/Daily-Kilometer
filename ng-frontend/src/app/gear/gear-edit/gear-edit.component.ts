import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

import { GearService } from '../../services/gear.service';

import { Gear } from '../../models/gear';

@Component({
  selector: 'app-gear-edit',
  templateUrl: './gear-edit.component.html',
  styleUrls: ['./gear-edit.component.css']
})
export class GearEditComponent implements OnInit {
  gear: Gear;

  constructor(private route: ActivatedRoute,
              private router: Router,
              private gearService: GearService) { }

  ngOnInit() {
    let id = this.route.snapshot.paramMap.get('id');
    this.gearService.get(+id).subscribe(gear => this.gear = gear);
  }

  submit(gear: Gear) {
    gear.pk = this.gear.pk;
    this.gearService.update_gear(gear).subscribe(() => {
      this.router.navigate(['gear']);
    });
  }
}
