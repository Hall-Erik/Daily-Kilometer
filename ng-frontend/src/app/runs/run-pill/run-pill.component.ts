import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { faEdit, faTrash } from '@fortawesome/free-solid-svg-icons';
import { faPaw, faRoad, faMountain, faStopwatch, faDungeon, faFlagCheckered } from '@fortawesome/free-solid-svg-icons';

import { UserService } from '../../services/user.service';
import { User } from '../../models/user';
import { Run } from '../../models/run';

@Component({
  selector: 'app-run-pill',
  templateUrl: './run-pill.component.html',
  styleUrls: ['./run-pill.component.css']
})
export class RunPillComponent implements OnInit {
  faTrash = faTrash;
  faEdit = faEdit;
  faPaw = faPaw;
  faRoad = faRoad;
  faMountain = faMountain;
  faStopwatch = faStopwatch;
  faDungeon = faDungeon;
  faFlagCheckered = faFlagCheckered;
  
  @Input() run: Run;
  @Output() runDelete = new EventEmitter<Run>();
  user: User = this.userService.user.getValue();

  constructor(private userService: UserService) { }

  get run_type() {
    switch (this.run.run_type) {
      case 'Canicross':
        return faPaw;
      case 'Road run':
        return faRoad;
      case 'Long run':
        return faStopwatch;
      case 'Trail run':
        return faMountain;
      case 'Race':
        return faFlagCheckered;
      case 'Treadmill':
        return faDungeon;
    }
    return '';
  }

  ngOnInit() {
    this.userService.user.subscribe(user => this.user = user);
  }

  onDelete() {
    this.runDelete.emit(this.run);
  }
}