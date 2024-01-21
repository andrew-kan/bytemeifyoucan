import {Component, Inject, Input} from '@angular/core';
import {
  MatDialog,
  MAT_DIALOG_DATA,
  MatDialogRef,
  MatDialogTitle,
  MatDialogContent,
  MatDialogActions,
  MatDialogClose,
} from '@angular/material/dialog';
import {MatButtonModule} from '@angular/material/button';
import {FormsModule} from '@angular/forms';
import {MatInputModule} from '@angular/material/input';
import {MatFormFieldModule} from '@angular/material/form-field';

export interface DialogData {
  subject: string;
  content: string;
  reply:string;
  from:string;
}

/**
 * @title Dialog Overview
 */
@Component({
  selector: 'dialog-overview-example',
  templateUrl: 'dialog-overview-example.html',
  standalone: true,
  styleUrl:'dialog-overview-example.css',
  imports: [MatFormFieldModule, MatInputModule, FormsModule, MatButtonModule],
})
export class DialogOverviewExample {

  @Input() email!:any;

  constructor(public dialog: MatDialog) {}

  openDialog(): void {
    const dialogRef = this.dialog.open(DialogOverviewExampleDialog, {
        width: '800px', // Set the width you want
        data: {subject: this.email['email']['Subject'], content: this.decodeBase64(this.email['email']['Content'][0]['$binary']["base64"]), reply:this.email["reply"][0]["reply"], from:this.email["email"]["From"]}
      });
      

    dialogRef.afterClosed().subscribe(result => {
      console.log('The dialog was closed');
    });
  }



  decodeBase64(b64Encoded:string) {
    // Decodes the base64 string into an "intermediate" binary string
    const binaryString = atob(b64Encoded);
  
    // Converts the binary string to a UTF-8-encoded string
    const bytes = new Uint8Array(binaryString.length);
    for (let i = 0; i < binaryString.length; i++) {
      bytes[i] = binaryString.charCodeAt(i);
    }
    const decodedStr = new TextDecoder('utf-8').decode(bytes);
  
    return decodedStr;
  }
}

@Component({
  selector: 'dialog-overview-example-dialog',
  templateUrl: 'dialog-overview-example-dialog.html',
  standalone: true,
  imports: [
    MatFormFieldModule,
    MatInputModule,
    FormsModule,
    MatButtonModule,
    MatDialogTitle,
    MatDialogContent,
    MatDialogActions,
    MatDialogClose,
  ],
})
export class DialogOverviewExampleDialog {
  constructor(
    public dialogRef: MatDialogRef<DialogOverviewExampleDialog>,
    @Inject(MAT_DIALOG_DATA) public data: DialogData,
  ) {}

  onNoClick(): void {
    this.dialogRef.close();
  }
}


/**  Copyright 2024 Google LLC. All Rights Reserved.
    Use of this source code is governed by an MIT-style license that
    can be found in the LICENSE file at https://angular.io/license */