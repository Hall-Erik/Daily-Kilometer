import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';

import { Run } from '../../models/run';
import { User } from '../../models/user';

import { UserService } from '../../services/user.service';

@Component({
  selector: 'app-run-form',
  templateUrl: './run-form.component.html',
  styleUrls: ['./run-form.component.css']
})
export class RunFormComponent implements OnInit {
  user: User = this.userService.user.getValue();

  @Output() runSubmit = new EventEmitter<Run>();

  @Input() set run(initial: Run) {
    if (initial) {
      this.runForm.patchValue(initial);
    }
  }

  runForm = this.fb.group({
    distance: ['', Validators.required],
    units: ['mi', Validators.required],
    hours: ['', [Validators.min(0)]],
    minutes: ['', [Validators.min(0), Validators.max(59)]],
    seconds: ['', [Validators.min(0), Validators.max(59)]],
    date: ['', Validators.required],
    gear: '',
    run_type: '',
    description: ''
  });

  get distance() { return this.runForm.get('distance'); }
  get units() { return this.runForm.get('units'); }
  get duration() {
    let hours = this.runForm.get('hours');
    let minutes = this.runForm.get('minutes');
    let seconds = this.runForm.get('seconds');
    if(!hours && !minutes && !seconds) {
      return null;
    }
    return null;
  }
  get hours() { return this.runForm.get('hours'); }
  get minutes() { return this.runForm.get('minutes'); }
  get seconds() { return this.runForm.get('seconds'); }
  get date() { return this.runForm.get('date'); }
  get gear() { return this.runForm.get('gear'); }
  get run_type() { return this.runForm.get('run_type'); }
  get description() { return this.runForm.get('description'); }

  constructor(private fb: FormBuilder,
              private userService: UserService) { }

  ngOnInit() {
    this.userService.user.subscribe(user => this.user = user);
    if (this.date.value === '') {
      let d = new Date();
      let date = '' + d.getDate();
      let month = '' + (d.getMonth() + 1);
      let year = d.getFullYear();

      if (month.length < 2) month = '0' + month;
      if (date.length < 2) date = '0' + date;

      this.date.patchValue([year, month, date].join('-'));
    }
  }

  get_duration(): string {
    if(this.hours.value === '' && this.minutes.value === ''
    && this.seconds.value === '') {
      return null;
    }

    let hours = (this.hours.value) ? '' + this.hours.value : '0';
    let minutes = (this.minutes.value) ? '' + this.minutes.value : '00';
    let seconds = (this.seconds.value) ? '' + this.seconds.value : '00';
    
    if(minutes.length < 2) minutes = '0' + minutes;
    if(seconds.length < 2) seconds = '0' + seconds;

    return [hours, minutes, seconds].join(':');
  }

  onSubmit() {
    let run = new Run(this.runForm.value);
    run.duration = this.get_duration();
    delete run['hours'];
    delete run['minutes'];
    delete run['seconds'];
    this.runSubmit.emit(run);
  }
}
