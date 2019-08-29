import { Component } from '@angular/core';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { faTimes } from '@fortawesome/free-solid-svg-icons';

import { AlertService } from '../../services/alert.service';
import { GearService } from '../../services/gear.service';

import { Gear } from '../../models/gear';

@Component({
  selector: 'app-gear-create',
  templateUrl: './gear-create.component.html',
  styleUrls: ['./gear-create.component.css']
})
export class GearCreateComponent {
  faTimes = faTimes;

  constructor(private gearService: GearService,
              private alertService: AlertService,
              public activeModal: NgbActiveModal) { }

  submit(gear: Gear) {
    this.gearService.create_gear(gear).subscribe(() => {
      this.alertService.clear();
      this.alertService.success("Shoe added.");
      this.activeModal.close();
    });
  }
}
