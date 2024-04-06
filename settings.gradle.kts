pluginManagement {
	repositories {
		maven { url = uri("https://repo.spring.io/milestone") }
		maven { url = uri("https://repo.spring.io/snapshot") }
		gradlePluginPortal()
	}
}
rootProject.name = "fc"
include("modules:fc-common")
findProject(":modules:fc-common")?.name = "fc-common"
include("modules:apps-data-publisher")
findProject(":modules:apps-data-publisher")?.name = "apps-data-publisher"
