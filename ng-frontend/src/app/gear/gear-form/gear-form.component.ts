import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';

import { Gear } from '../../models/gear';
import { User } from '../../models/user';

import { UserService } from '../../services/user.service';

@Component({
  selector: 'app-gear-form',
  templateUrl: './gear-form.component.html',
  styleUrls: ['./gear-form.component.css']
})
export class GearFormComponent implements OnInit {
  user: User = this.userService.user.getValue();

  @Output() gearSubmit = new EventEmitter<Gear>();
  
  @Input() set gear(initial: Gear) {
    if (initial) {
      this.gearForm.patchValue(initial);
      this.date_added.patchValue(this.get_date_string(initial.date_added));
      if (initial.date_retired) {
        this.date_retired.patchValue(this.get_date_string(initial.date_retired));
      }
    }
  }

  gearForm = this.fb.group({
    name: ['', Validators.required],
    start_distance: [0, [Validators.required, Validators.min(0)]],
    start_units: ['mi', Validators.required],
    date_added: ['', Validators.required],
    date_retired: ''
  });

  get name() { return this.gearForm.get('name'); }
  get start_distance() { return this.gearForm.get('start_distance'); }
  get start_units() { return this.gearForm.get('start_units'); }
  get date_added() { return this.gearForm.get('date_added'); }
  get date_retired() { return this.gearForm.get('date_retired'); }

  constructor(private fb: FormBuilder,
              private userService: UserService) { }

  ngOnInit() {
    this.userService.user.subscribe(user => this.user = user);
    if (this.date_added.value === '') {
      this.date_added.patchValue(this.get_date_string());
    }
  }

  get_date_string(initial?: string): string {
    let d: Date;
    if(initial) {
      d = new Date(initial);
    } else {
      d = new Date();
    }
    let date = '' + d.getDate();
    let month = '' + (d.getMonth() + 1);
    let year = d.getFullYear();

    if (month.length < 2) month = '0' + month;
    if (date.length < 2) date = '0' + date;

    return [year, month, date].join('-');
  }

  onSubmit() {
    let gear = new Gear(this.gearForm.value);
    if(this.date_added.value !== '') {
      gear.date_added = this.date_added.value + 'T00:00:00';
    }
    if(this.date_retired.value !== '') {
      gear.date_retired = this.date_retired.value + 'T00:00:00';
    } else {
      gear.date_retired = null;
    }
    this.gearSubmit.emit(gear);
  }
}
