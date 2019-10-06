<template>
    <div>
        <footer class="footer" v-once>Copyright &copy; {{ getYear }} Gerapy All Rights Reserved

            <lang-switch></lang-switch>
        </footer>
    </div>
</template>
<script>
    /* eslint-disable */
    import LangSwitch from './LangSwitch'

    export default {
        components: {LangSwitch},
        computed: {
            getYear() {
                return new Date().getFullYear()
            }
        },
        comments: {
            LangSwitch
        }
    }
</script>
