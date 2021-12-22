<template>
  <div>
    <v-dialog v-model="dialogSync" persistent max-width="600px">
      <v-form ref="form">
        <v-card>
          <v-card-title>
            <span class="text-h5">Wgraj zdjęcie</span>
          </v-card-title>
          <v-card-text>
            <v-file-input
              :rules="[(f) => !!f || 'Brak pliku']"
              v-model="file"
              accept="image/*"
              label="Zdjęcie"
            ></v-file-input>
            <v-img v-if="isFileLoaded" :src="fileSource"></v-img>
          </v-card-text>
          <v-card-actions>
            <v-btn color="error" tile @click="dialogSync = false">
              Close
            </v-btn>
            <v-spacer></v-spacer>
            <v-btn color="success" tile @click="saveImage()"> Save </v-btn>
          </v-card-actions>
        </v-card>
      </v-form>
    </v-dialog>
  </div>
</template>

<script lang="ts">
import { addImageImageAddImagePost } from "@/api";
import { Component, PropSync, Vue, Watch } from "vue-property-decorator";

@Component({ components: {} })
export default class ImportImage extends Vue {
  @PropSync("dialog", { type: Boolean }) dialogSync!: boolean;

  file: File | null = null;
  fileSource: any = null;
  isFileLoaded: boolean = false;

  @Watch("file")
  onFileChanged() {
    this.fileSource = URL.createObjectURL(this.file);
    this.isFileLoaded = true;
  }

  async saveImage() {
    if ((this.$refs["form"] as any).validate() == false) return;
    console.log(this.fileSource);
    let fileContent = await this.getBase64(this.file);
    await addImageImageAddImagePost({
      body: {
        name: this.file?.name!,
        content: fileContent as string,
      },
    });

    this.dialogSync = false;
  }

  getBase64(file: any) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => resolve(reader.result);
      reader.onerror = (error) => reject(error);
    });
  }
}
</script>

<style scoped></style>
