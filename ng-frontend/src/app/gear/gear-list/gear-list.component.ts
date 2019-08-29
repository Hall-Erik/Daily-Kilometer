import { Component, OnInit } from '@angular/core';
import { faEdit, faTrash } from '@fortawesome/free-solid-svg-icons';

import { NgbModal } from '@ng-bootstrap/ng-bootstrap';

import { GearCreateComponent } from '../gear-create/gear-create.component';
import { GearEditComponent } from '../gear-edit/gear-edit.component';

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
              private alertService: AlertService,
              private modalService: NgbModal) { }

  ngOnInit() {
    this.gearService.get_gear().subscribe(gear => this.gear = gear);
  }

  add_gear() {
    const modalRef = this.modalService.open(GearCreateComponent);
    modalRef.result.then(() => {
      this.gearService.get_gear().subscribe(gear => this.gear = gear);
    });
  }

  edit_gear(gear: Gear) {
    const modalRef = this.modalService.open(GearEditComponent);
    modalRef.componentInstance.gear = gear;
    modalRef.result.then(() => {
      this.gearService.get_gear().subscribe(gear => this.gear = gear);
    });
  }

  delete(id: number) {
    if (confirm('Are you sure you want to delete this shoe?')) {
      this.gearService.delete_gear(id).subscribe(() => {
        this.gearService.get_gear().subscribe(gear => this.gear = gear);
        this.alertService.clear();
        this.alertService.success("Shoe deleted.");
      });
    }
  }
}
