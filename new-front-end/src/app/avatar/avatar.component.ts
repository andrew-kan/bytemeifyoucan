import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-avatar',
  standalone: true,
  imports: [],
  templateUrl: './avatar.component.html',
  styleUrl: './avatar.component.css'
})
export class AvatarComponent {


@Input() inputString!:string;

imagePath!: string;


ngOnInit() {
  this.imagePath = this.hashString(this.inputString);
}




hashString(inputString: string): string {
    let hash = 0;
    if (inputString.length === 0) {
      return "assets/"+hash+".jpeg";
    }
    for (let i = 0; i < inputString.length; i++) {
      const char = inputString.charCodeAt(i);
      hash = (hash << 5) - hash + char;
      hash = hash & hash; // Convert to 32bit integer
    }
    let n = Math.abs(hash % 11) + 1; // Return a number between 1 and 11
    return "assets/" +n+".jpeg"
  }


}
function ngOnInit(): (target: AvatarComponent, propertyKey: "") => void {
  throw new Error('Function not implemented.');
}

