import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { faEdit, faTrash } from '@fortawesome/free-solid-svg-icons';

import { UserService } from '../../services/user.service';
import { User } from '../../models/user';
import { Run } from '../../models/run';

@Component({
  selector: 'app-run-pill',
  templateUrl: './run-pill.component.html',
  styleUrls: ['./run-pill.component.css']
})
export class RunPillComponent implements OnInit {
  faTrash = faTrash
  faEdit = faEdit
  
  @Input() run: Run;
  @Output() runDelete = new EventEmitter<Run>();
  user: User;

  constructor(private userService: UserService) { }

  ngOnInit() {
    this.user = this.userService.user.getValue();
    this.userService.user.subscribe(user => this.user = user);
  }

  onDelete() {
    this.runDelete.emit(this.run);
  }
}
