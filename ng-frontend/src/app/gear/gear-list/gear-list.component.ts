import { Component, OnInit } from '@angular/core';
import { faEdit, faTrash } from '@fortawesome/free-solid-svg-icons';

import { AlertService } from '../../services/alert.service';
import { GearService } from '../../services/gear.service';

import { Gear } from '../../models/gear';

@Component({
  selector: 'app-gear-list',
  templateUrl: './gear-list.component.html',
  styleUrls: ['./gear-list.component.css']
})
export class GearListComponent implements OnInit {
  faEdit = faEdit;
  faTrash = faTrash;
  
  gear: Gear[];

  constructor(private gearService: GearService,
              private alertService: AlertService) { }

  ngOnInit() {
    this.gearService.get_gear().subscribe(gear => this.gear = gear);
  }

  delete(id: number) {
    if (confirm('Are you sure you want to delete this shoe?')) {
      this.gearService.delete_gear(id).subscribe(() => {
        this.gearService.get_gear().subscribe(gear => this.gear = gear);
        this.alertService.success("Shoe deleted.");
      });
    }
  }
}
