<script setup lang="ts">
defineProps(['formData', 'errors', 'touched', 'markAsTouched', 'validateField', 'activateCallback']);
</script>

<template>
  <div class="card flex justify-center">
    <div class="flex flex-col gap-4 w-full">
      <div class="font-semibold text-xl">Primeiro Nome*</div>
      <InputText
        id="first_name"
        v-keyfilter.alpha
        v-model="formData.first_name"
        :invalid="touched.first_name && !!errors.first_name"
        @blur="markAsTouched('first_name'); validateField('first_name')"
        placeholder="Introduza o primeiro nome"
      />
      <small class="text-red-500" v-if="touched.first_name && errors.first_name">
        {{ errors.first_name }}
      </small>

      <div class="font-semibold text-xl">Ultimo Nome*</div>
      <InputText
        id="last_name"
        v-keyfilter.alpha
        v-model="formData.last_name"
        :invalid="touched.last_name && !!errors.last_name"
        @blur="markAsTouched('last_name'); validateField('last_name')"
        placeholder="Introduza o ultimo nome"
      />
      <small class="text-red-500" v-if="touched.last_name && errors.last_name">
        {{ errors.last_name }}
      </small>

      <div class="font-semibold text-xl">Email*</div>
      <InputText
        id="email"
        v-model="formData.email"
        :invalid="touched.email && !!errors.email"
        @blur="markAsTouched('email'); validateField('email')"
        placeholder="Introduza o email"
      />
      <small class="text-red-500" v-if="touched.email && errors.email">
        {{ errors.email }}
      </small>

      <div class="font-semibold text-xl">Password*</div>
      <Password 
        id="password"
        v-model="formData.password"
        :invalid="touched.password && !!errors.password"
        @blur="markAsTouched('password'); validateField('password')"
        toggleMask
        placeholder="Introduza a password"
      >
        <template #header>
          <div class="font-semibold text-xm mb-4">Escolha uma password</div>
        </template>
        <template #footer>
          <Divider />
          <ul class="pl-2 ml-2 my-0 leading-normal">
            <li>Minimo de 6 caracteres.</li>
          </ul>
        </template>
      </Password>
      <small class="text-red-500" v-if="touched.password && errors.password">
        {{ errors.password }}
      </small>

      <div class="font-semibold text-xl">Telefone*</div>
      <InputMask
        id="phone"
        mask="999 999 999"
        v-model="formData.phone"
        :invalid="touched.phone && !!errors.phone"
        @blur="markAsTouched('phone'); validateField('phone')"
        placeholder="Introduza o telefone"
      />
      <small class="text-red-500" v-if="touched.phone && errors.phone">
        {{ errors.phone }}
      </small>

      <div class="font-semibold text-xl">Imagem de Perfil*</div>
      <InputText
        id="img_src"
        v-model="formData.img_src"
        :invalid="touched.img_src && !!errors.img_src"
        @blur="markAsTouched('img_src'); validateField('img_src')"
        placeholder="Introduza a URL da imagem de perfil (png, jpg, svg)"
      />
      <small class="text-red-500" v-if="touched.img_src && errors.img_src">
        {{ errors.img_src }}
      </small>
      <div v-if="formData.img_src" class="flex justify-center pt-4">
        <img
          :src="formData.img_src"
          alt="Imagem de Perfil"
          class="max-h-40 rounded-md shadow-md"
          @error="formData.img_src = ''; errors.img_src = 'A URL fornecida não carrega uma imagem válida.'"
        />
      </div>

      <div class="font-semibold text-xl">Data de nascimento*</div>
      <DatePicker
        id="birth_date"
        v-model="formData.birth_date"
        :invalid="touched.birth_date && !!errors.birth_date"
        @blur="markAsTouched('birth_date'); validateField('birth_date')"
        dateFormat="dd-mm-yy"
      />
      <small class="text-red-500" v-if="touched.birth_date && errors.birth_date">
        {{ errors.birth_date }}
      </small>

      <div class="text-sm text-gray-500 pt-2">
        Os campos marcados com <span class="text-red-500">*</span> são obrigatórios.
      </div>

      <div class="flex justify-end pt-4">
        <Button label="Proximo" icon="pi pi-arrow-right" iconPos="right" @click="activateCallback('2')" />
        <Button type="submit" label="Submeter" icon="pi pi-check" />
      </div>
    </div>
  </div>
</template>