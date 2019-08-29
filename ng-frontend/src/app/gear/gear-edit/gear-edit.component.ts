import { Component, Input } from '@angular/core';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { faTimes } from '@fortawesome/free-solid-svg-icons';

import { AlertService } from '../../services/alert.service';
import { GearService } from '../../services/gear.service';

import { Gear } from '../../models/gear';

@Component({
  selector: 'app-gear-edit',
  templateUrl: './gear-edit.component.html',
  styleUrls: ['./gear-edit.component.css']
})
export class GearEditComponent {
  faTimes = faTimes;

  @Input() gear: Gear;

  constructor(private gearService: GearService,
              private alertService: AlertService,
              public activeModal: NgbActiveModal) { }

  submit(gear: Gear) {
    gear.pk = this.gear.pk;
    this.gearService.update_gear(gear).subscribe(() => {
      this.alertService.clear();
      this.alertService.success("Shoe updated.");
      this.activeModal.close();
    });
  }
}
