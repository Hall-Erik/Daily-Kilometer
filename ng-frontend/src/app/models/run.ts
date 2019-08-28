import { Gear } from './gear';
import { User } from './user';

export class RunList {
    results: Run[];
    next: string;

    public constructor(init?: Partial<RunList>) {
        Object.assign(this, init);
    }
}

export class Run {
    pk: number;
    run_date: string;
    distance: number;
    units: string;
    duration: string;
    description: string;
    run_type: string;
    gear: Gear;
    user: User;

    get_duration: number;
    get_pace: number;

    public constructor(init?: Partial<Run>) {
        Object.assign(this, init);
    }
}